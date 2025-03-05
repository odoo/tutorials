# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta

class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = "Real Estate Property Offer"
    _sql_constraints = [
        ('check_positive_value_offer_price', 'CHECK(price >= 0)',
         'Offer price must be positive')
    ]

    price = fields.Float(string="Price", required=True)
    status = fields.Selection(
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
        ],
        string="Status",
        copy=False
    )
    partner_id = fields.Many2one('res.partner', string="Partner", required=True)
    property_id = fields.Many2one('estate.property', required=True, ondelete='cascade')
    validity = fields.Integer(string="validity", default=7)
    date_deadline = fields.Date(string="valid till", compute='_compute_date_deadline', inverse='_inverse_date_deadline')
    property_type_id = fields.Many2one(related='property_id.property_type_id')

    @api.depends('validity')
    def _compute_date_deadline(self):
        for offer in self:
            offer.date_deadline = fields.Date.today() + relativedelta(days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            offer.validity = (offer.date_deadline - fields.Date.today()).days

    def action_offer_accept(self):
        for offer in self:
            if 'accepted' in offer.property_id.offer_ids.mapped('status'):
                raise UserError(_("Offer is already accepted for this property"))
            else :
                offer.status = 'accepted'
                offer.property_id.buyer_id = offer.partner_id
                offer.property_id.selling_price = offer.price
                offer.property_id.state = 'offer accepted'
                for property_offer in offer.property_id.offer_ids:
                    if property_offer != offer:
                        property_offer.status = 'refused'
        return True

    def action_offer_refuse(self):
        for offer in self:
            if offer.status == 'accepted':
                offer.property_id.buyer_id = ''
                offer.property_id.selling_price = 0.0
            offer.status = 'refused'
        return True

    @api.model_create_multi
    def create(self, vals_list):
        for offer in vals_list:
            property = self.env['estate.property'].browse(offer['property_id'])
            if property.state != 'offer received':
                property.state = 'offer received'
            max_offer = 0
            if property.offer_ids:
                max_offer = max(property.offer_ids.mapped('price'))
            if max_offer > offer['price']:
                    raise UserError(_(f"The new offer must be higher than or equal to the maximum offer of {max_offer:.2f}"))
        return super().create(vals_list)

    def action_property_offer_accept(self):
        self.property_id.selling_price = self.price
        self.property_id.buyer_id = self.partner_id
        for offer in self.property_id.offer_ids:
            if offer == self:
                offer.status = 'accepted'
                self.property_id.state = 'offer accepted'
            else:
                offer.status = 'refused'
        return True
