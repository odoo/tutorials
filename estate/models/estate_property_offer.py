# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api
from datetime import date, timedelta


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'
    _order = "price desc"

    price = fields.Float(string='Price')
    status = fields.Selection(string='Status', copy=False,
                            selection=[('accepted', 'Accepted'), ('refused', 'Refused')])
    partner_id = fields.Many2one('res.partner', string='Customer', required=True)
    property_id = fields.Many2one('estate.property', string='Property', required=True)
    validity = fields.Integer(string='Validity (days)', default=7)
    date_deadline = fields.Date(string='Deadline', compute='_compute_deadline', inverse='_inverse_deadline')
    property_type_id = fields.Many2one('estate.property.type', string='Property Type', related="property_id.property_type_id", store=True)

    _check_price = models.Constraint(
        'CHECK(price > 0)',
        'The offer price must be strictly positive',
    )

    @api.depends('validity')
    def _compute_deadline(self):
        for record in self:
            record.date_deadline = (record.create_date if record.create_date else date.today()) + timedelta(days=record.validity)

    def _inverse_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - (record.create_date.date() if record.create_date else date.today())).days

    def action_accept(self):
        for record in self:
            if record.property_id.state in ('new', 'offer_received'):
                record.property_id.state = 'offer_accepted'
                record.status = 'accepted'
                record.property_id.selling_price = record.price
                record.property_id.buyer_id = record.partner_id
        return True

    def action_refuse(self):
        for record in self:
            if not record.status:
                record.status = 'refused'
        return True
