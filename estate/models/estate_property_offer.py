# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from odoo.exceptions import UserError

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price desc"
    _sql_constraints = [
        ('check_price', 'CHECK(price > 0)', 'Offer price must be strictly positive!'),
    ]

    price = fields.Float(string='Price')
    status = fields.Selection(
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused')
        ],
        string='Status',
        copy=False
    )
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    property_id = fields.Many2one('estate.property', string='Property', required=True)
    validity = fields.Integer(string='Validity (days)', default=7)
    date_deadline = fields.Date(string='Deadline', compute='_compute_date_deadline', inverse='_inverse_date_deadline')
    property_type_id = fields.Many2one('estate.property.type', string='Property Type', related='property_id.property_type_id')
    @api.depends('validity')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = fields.Date.add(record.create_date, days=record.validity)
            else:
                record.date_deadline = fields.Date.add(fields.Date.today(), days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - fields.Date.to_date(record.create_date)).days

    def action_accept_offer(self):
        for record in self:
            if 'accepted' not in record.property_id.offer_ids.mapped('status'):
                record.status = 'accepted'
                record.property_id.state = 'offer_accepted'
                record.property_id.selling_price = record.price
                record.property_id.partner_id = record.partner_id
            else:
                raise UserError("This property already has an accepted offer.")

    def action_refuse_offer(self):
        for record in self:
            record.status = 'refused'

    @api.model_create_multi
    def create(self, vals_list):
        for record in vals_list:
            property = self.env['estate.property'].browse(record.get('property_id'))

            if property.state == 'sold':
                raise UserError("Property is already sold.")

            if property.best_price > record.get('price'):
                raise UserError("Offer price can't be less than the current best offer.")

            property.state = 'offer_received'
        return super().create(vals_list)
