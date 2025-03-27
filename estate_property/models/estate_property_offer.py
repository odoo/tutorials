from datetime import timedelta

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Real Estate Property Offer'
    _order = 'price desc'
    _sql_constraints = [
        (
            'offer_price_strictly_positive',
            'CHECK(price > 0)',
            'Offer price must be strictly positive',
        ),
    ]

    date_deadline = fields.Date(
        compute='_compute_date_deadline',
        inverse='_inverse_date_deadline',
        string='Date Deadline',
    )
    price = fields.Float()
    validity = fields.Integer(default=7, string='Validity (days)')
    status = fields.Selection(
        [('accepted', 'Accepted'), ('refused', 'Refused')],
        copy=False,
    )
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    property_type_id = fields.Many2one(related='property_id.property_type_id', store=True)

    @api.depends('validity')
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = (record.create_date.date() or fields.Date.now()) + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline -(record.create_date.date() or fields.Date.now())).days

    @api.model
    def create(self, vals):
        property_id = vals.get('property_id')

        property = self.env['estate.property'].browse(property_id)

        property.state = 'offer_received'

        existing_offers = self.env['estate.property.offer'].search([('property_id', '=', property_id), ('price', '>=', vals['price'])])

        if existing_offers:
            raise ValidationError("The offer value must be higher than existing offers.")

        return super().create(vals)

    def action_accept_offer(self):
        for record in self:
            record.status = 'accepted'

    def action_refuse_offer(self):
        for record in self:
            record.status = 'refused'
