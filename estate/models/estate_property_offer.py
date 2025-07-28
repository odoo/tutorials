from dateutil.relativedelta import relativedelta
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = "Estate Property Offers"
    _order = 'price desc'

    _sql_constraints = [
        ('check_price', 'CHECK(price > 0)', "Offer Price should be bigger than 0"),
    ]

    price = fields.Float()
    status = fields.Selection(
        selection=[
            ('accepted', "Accepted"),
            ('refused', "Refused"),
        ]
    )
    partner_id = fields.Many2one('res.partner', string="Partner", required=True)
    property_id = fields.Many2one('estate.property', string="Property", required=True)
    type_id = fields.Many2one(related='property_id.type_id')
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute='_compute_date_deadline', inverse='_inverse_date_deadline')

    @api.depends('validity', 'create_date')
    def _compute_date_deadline(self):
        for offer in self:
            offer.date_deadline = (offer.create_date or fields.Date.today()) + relativedelta(days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            offer.validity = (offer.date_deadline - offer.create_date.date()).days

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            property_id = self.env['estate.property'].browse(vals['property_id'])
            if vals['price'] < property_id.best_offer:
                raise UserError(_("Cannot input price lower than current best offer"))
            property_id.state = 'offer_received'

        return super().create(vals_list)

    def action_accept(self):
        for offer in self:
            if any(r == 'accepted' for r in offer.property_id.offer_ids.mapped('status')):
                raise UserError(_("Another offer was already accepted"))
            offer.status = 'accepted'
            offer.property_id.selling_price = offer.price
            offer.property_id.partner_id = offer.partner_id

    def action_refuse(self):
        for offer in self:
            offer.status = 'refused'
