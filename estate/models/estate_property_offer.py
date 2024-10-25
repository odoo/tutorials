from datetime import timedelta
from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools import float_compare


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Model representing the offers from partners to a specific property'
    _order = 'price desc'

    price = fields.Float(string="Price")
    status = fields.Selection(
        string="Status",
        copy=False,
        selection=[
            ('accepted', "Accepted"),
            ('refused', "Refused")
        ]
    )
    partner_id = fields.Many2one('res.partner', string="Partner", required=True)
    property_id = fields.Many2one('estate.property', string="Property", required=True)
    validity = fields.Integer(string="Validity", default=7)
    date_deadline = fields.Date(compute='_compute_date_deadline', inverse='_inverse_date_deadline', string="Date Deadline")
    create_date = fields.Date(default=lambda self: fields.Datetime.now(), string="Create Date")
    property_type_id = fields.Many2one(related="property_id.property_type_id", string="Property Type ID")

    _sql_constraints = [
        ('check_offer_price', 'CHECK(price > 0)',
         "The offer price should be greater than 0."),
    ]

    @api.depends('validity', 'create_date')
    def _compute_date_deadline(self):
        for offer in self:
            offer.date_deadline = offer.create_date + timedelta(days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            delta = offer.date_deadline - offer.create_date
            offer.validity = delta.days

    def action_confirm(self):
        self.ensure_one()

        if self.status == 'accepted':
            raise UserError(_("Offer already accepted!"))
        elif self.status == 'refused':
            raise UserError(_("Can't accept a refused offer!"))
        elif self.property_id.buyer_id:
            raise UserError(_("Can't accept more than 1 offer!"))
        else:
            if float_compare(self.price, 0.9 * self.property_id.expected_price, 5) == -1:
                raise UserError(_("Selling price cannot be lower than 90% of the expected price!"))

            self.status = 'accepted'
            self.property_id.state = 'offer_accepted'
            self.property_id.selling_price = self.price
            self.property_id.buyer_id = self.partner_id

        return True

    def action_refuse(self):
        for offer in self:
            if offer.status == 'refused':
                raise UserError(_("Offer already refused!"))
            elif offer.status == 'accepted':
                raise UserError(_("Can't refuse an accepted offer!"))
            else:
                offer.status = 'refused'

        return True

    @api.model_create_multi
    def create(self, vals):
        for val in vals:
            current_property_id = self.env['estate.property'].browse(val['property_id'])

            if current_property_id.best_price > val['price']:
                raise UserError(_("Can't create an offer with a price lower than the best offer!"))

            current_property_id.state = 'offer_received'

        return super().create(vals)
