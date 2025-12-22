# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import timedelta
from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = "Real Estate Property Offer"
    _order = 'price desc'

    _check_price = models.Constraint('Check(price > 0)', "The offer price must be strictly positive.")

    price = fields.Float(required=True, string="Price")
    status = fields.Selection(selection=[('accepted', "Accepted"), ('refused', "Refused")], copy=False, string="Status")
    partner_id = fields.Many2one(comodel_name='res.partner', string="Partner", required=True)
    property_id = fields.Many2one(comodel_name='estate.property', string="Property", required=True, ondelete='cascade')
    validity = fields.Integer(default=7, string="Validity (days)")
    date_deadline = fields.Date(
        compute='_compute_date_deadline',
        inverse='_inverse_date_deadline',
        store=True,
        string="Deadline",
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            property_id = vals.get('property_id')
            price = vals.get('price')

            if property_id and price:
                property = self.env['estate.property'].browse(property_id)
                if property.offer_ids:
                    max_offer = max(property.offer_ids.mapped('price'))
                    if price < max_offer:
                        raise UserError(self.env._("The offer amount must be higher than %.2f") % max_offer)

        offers = super().create(vals_list)
        for offer in offers:
            if offer.property_id.state == 'new':
                offer.property_id.state = 'offer_received'
        return offers

    @api.depends('validity')
    def _compute_date_deadline(self):
        for offer in self:
            offer.date_deadline = fields.Date.today() + timedelta(days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            if offer.date_deadline:
                offer.validity = (offer.date_deadline - fields.Date.today()).days

    def action_accept(self):
        for offer in self:
            if offer.property_id.offer_ids.filtered(lambda o: o.status == 'accepted' and o.id != offer.id):
                raise UserError(self.env._("Only one offer can be accepted per property."))
            offer.status = 'accepted'
            offer.property_id.buyer_id = offer.partner_id
            offer.property_id.selling_price = offer.price
            offer.property_id.state = 'offer_accepted'
        return True

    def action_refuse(self):
        for offer in self:
            offer.status = 'refused'
        return True
