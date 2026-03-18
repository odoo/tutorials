# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, exceptions
from dateutil.relativedelta import relativedelta


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate property offer"

    price = fields.Float()
    _check_price = models.Constraint(
        'CHECK(price > 0)',
        'The offer price of must be strictly positive!'
    )
    status = fields.Selection(copy=False, selection=[('accepted', 'Accepted'), ('refused', 'Refused')])
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    property_id = fields.Many2one('estate.property', string='Property', required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline")

    @api.depends('validity')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date+relativedelta(days=record.validity)
            else:
                record.date_deadline = fields.Date.today()+relativedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline-fields.Date.to_date(record.create_date)).days

    def action_accept_offer(self):
        for record in self:
            if record.status == 'accepted':
                continue
            for offer in record.property_id.offer_ids:
                if offer.status == 'accepted':
                    offer.status = 'refused'
            record.status = 'accepted'
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price

    
    def action_refuse_offer(self):
        for record in self:
            record.status = 'refused'