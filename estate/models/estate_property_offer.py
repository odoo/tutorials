# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api
from datetime import timedelta

class EstatePropertyOffer(models.Model):
    _name = "estate_property_offer"
    _description = "Estate Property Offer"
    _order = "price desc"

    price = fields.Float('Price')
    _positive_offer_price = models.Constraint("Check(price > 0)", "Offer price must be positive.")
    status = fields.Selection([('accepted', 'Accepted'), ('refused', 'Refused')], string='Status', copy=False)
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    property_id = fields.Many2one('estate_property', string='Property', required=True)

    validity = fields.Integer('Validity', compute="_compute_validity", inverse="_inverse_validity", default=7, help="Validity in days")
    create_date = fields.Datetime('Creation Date', default=fields.Datetime.now, readonly=True)
    date_deadline = fields.Date('Date Deadline')

    property_type_id = fields.Many2one('estate_property_type', string='Property Type', related='property_id.property_type_id', store=True)

    @api.depends("date_deadline")
    def _compute_validity(self):
        for record in self:
            if record.date_deadline:
                if record.create_date:
                    record.validity = (record.date_deadline - record.create_date.date()).days
                else:
                    record.validity = (record.date_deadline - fields.Date.today()).days
            else:
                record.validity = 0

    def _inverse_validity(self):
        for record in self:
            if record.validity:
                if record.create_date:
                    record.date_deadline = record.create_date.date() + timedelta(days=record.validity)
                else:
                    record.date_deadline = fields.Date.today() + timedelta(days=record.validity)
            else:
                record.date_deadline = None

    active = fields.Boolean('Active', default=True)
    sequence = fields.Integer('Sequence', default=10)

    def action_accept(self):
        for record in self:
            record.status = 'accepted'
            record.property_id.state = 'offer_accepted'
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id
    
    def action_refuse(self):
        for record in self:
            record.status = 'refused'

