# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import timedelta
from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'
    _order = 'price desc'

    price = fields.Float(string='Offer Price')
    status = fields.Selection(
        string='Status',
        copy=False,
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused')
        ])
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    created_date = fields.Date(default=fields.Date.context_today, string='Created Date')
    validity = fields.Integer(default=7, string='Validity (Days)')
    date_deadline = fields.Date(compute='_compute_date_deadline', inverse='_inverse_date_deadline', string='Deadline Date', store='True')
    property_type_id = fields.Many2one(related='property_id.property_type_id', store=True)

    _sql_constraints = [
        ('price', 'CHECK(price >= 0)', 'Offer price must be strictly positive')
    ]

    @api.depends('created_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            if record.created_date and record.validity:
                record.date_deadline = record.created_date + timedelta(days=record.validity)
            else:
                record.date_deadline = False

    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline and record.created_date:
                record.validity = (record.date_deadline - record.created_date).days
            else:
                record.validity = 0

    def offer_accepted_action(self):
        for record in self:
            existing_offer = self.search([('property_id', '=', record.property_id.id), ('status', '=', 'accepted')])
            if existing_offer:
                raise UserError("This property already has an accepted offer.")
            property_record = record.property_id
            property_record.selling_price = record.price
            property_record.buyer_id = record.partner_id
            record.status = 'accepted'
            property_record.state = 'offer_accepted'
        return True

    def offer_refused_action(self):
        for record in self:
            record.status = 'refused'
        return True
