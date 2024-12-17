# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api
from datetime import timedelta, datetime
from odoo.exceptions import UserError

class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Manage different offers from buyers for a specific property."

    price = fields.Float(string="Price", required=True)

    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(string="Deadline", compute="_compute_deadline",
                                inverse="_inverse_deadline")

    status = fields.Selection([('accepted', 'Accepted'),
                               ('refused', 'Refused')],
                               copy=False)

    partner_id = fields.Many2one(
        'res.partner',
        string='Buyer',
        required=True
    )

    property_id = fields.Many2one(
        'estate.property',
        string='Property',
        required=True
    )

    @api.depends("validity", "create_date")
    def _compute_deadline(self):
        for record in self:
            create_date = record.create_date if record.create_date else datetime.now()
            record.date_deadline = create_date + timedelta(days=record.validity)

    def _inverse_deadline(self):
        for record in self:
            create_date = record.create_date if record.create_date else datetime.now()
            record.validity = (record.date_deadline - create_date.date()).days

    def accept_offer(self):
        for record in self:
            if record.status == 'accepted':
                raise UserError('This offer has already been accepted.')

            offer_prop = record.property_id
            accepted_off = offer_prop.offer_ids.filtered(lambda x: x.status == 'accepted')

            if accepted_off:
                raise UserError('This property has already accepted an offer.')
            
            offer_prop.property_buyer_id = record.partner_id
            offer_prop.selling_price =record.price

            record.status = 'accepted'
        return True
    
    def reject_offer(self):
        for record in self:
            if record.status == 'accepted':
                print("Yes")
                record.property_id.property_buyer_id = False
                record.property_id.selling_price = False
            record.status = 'refused'
        return True