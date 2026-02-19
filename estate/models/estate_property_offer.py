# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import timedelta

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate property offers"
    _order = "price desc"

    price = fields.Float('Price')
    status = fields.Selection(
        string='Status',
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
        copy=False)
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    property_id = fields.Many2one('estate.property', string='Property', required=True, ondelete='cascade')
    validity = fields.Integer('Validity (days)', default=7)
    date_deadline = fields.Date('Deadline', compute='_compute_date_deadline', inverse='_inverse_date_deadline')
    property_type_id = fields.Many2one(related='property_id.property_type_id', store=True)

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for offer in self:
            if offer.create_date:
                offer.date_deadline = offer.create_date + timedelta(days=offer.validity)
            else:
                offer.date_deadline = fields.Date.today() + timedelta(days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            offer.validity = (offer.date_deadline - offer.create_date.date()).days

    def action_accept_offer(self):
        for record in self:
            record.status = 'accepted'
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id
            record.property_id.state = 'offer_accepted'

    def action_refuse_offer(self):
        for record in self:
            record.status = 'refused'

    _check_positive_offer_price = models.Constraint(
        'CHECK(price > 0)',
        'The price of an offer should be strictly positive.',
    )

    @api.model
    def create(self, vals):
        if len(vals) == 0:
            return super().create(vals)
        property_id = vals[0].get('property_id')
        price = vals[0].get('price')
        if property_id and price:
            property_record = self.env['estate.property'].browse(property_id)
            if property_record.best_price and price <= property_record.best_price:
                error_msg = "The offer price should be higher than the best offer of the property."
                raise ValidationError(error_msg)
            property_record.state = 'offer_received'
        return super().create(vals)
