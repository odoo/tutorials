from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = "Estate Property Offer"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(
        selection=[('accepted', "Accepted"), ('refused', "Refused")], copy=False
    )
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        "Deadline", compute='_compute_date_deadline', inverse='_inverse_date_deadline'
    )
    _offer_price_check = models.Constraint(
        'CHECK(price >= 0)', "Offer price should be strictly positive"
    )
    property_type_id = fields.Many2one(
        related='property_id.property_type_id', store=True)

    # DEPENDS DECORATOR
    @api.depends('validity', 'create_date')
    def _compute_date_deadline(self):
        for record in self:
            start_date = (
                record.create_date.date() if record.create_date else fields.Date.today()
            )
            record.date_deadline = start_date + \
                relativedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            start_date = (
                record.create_date.date() if record.create_date else fields.Date.today()
            )
            record.validity = (record.date_deadline - start_date).days

    # BUTTON ACTION - OFFER
    def action_accept(self):
        if self.property_id.state == 'offer_accepted':
            raise UserError(
                _("An offer has already been accepted for this property.")
            )
        self.write({'status': 'accepted'})
        for offer in self:
            offer.property_id.write({
                'buyer_id': offer.partner_id.id,
                'selling_price': offer.price,
                'state': 'sold',
                'active': False
            })

    def action_refuse(self):
        for record in self:
            record.status = 'refused'
            record.property_id.write({
                'buyer_id': None,
                'selling_price': None,
            })

    @api.model_create_multi
    def create(self, vals_list):
        if not vals_list:
            return super().create(vals_list)
        property_id = vals_list[0].get('property_id')
        new_prices = [vals.get('price', 0) for vals in vals_list]
        max_new_price = max(new_prices)
        existing_offers = self.env['estate.property.offer'].search([
            ('property_id', '=', property_id)
        ])
        max_db_price = max(existing_offers.mapped(
            'price')) if existing_offers else 0
        if max_new_price <= max_db_price:
            raise UserError(
                "Offer price should be higher then the Existing One!"
            )
        self.env['estate.property'].browse(
            property_id).state = 'offer_received'

        return super().create(vals_list)
