# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api
from dateutil.relativedelta import relativedelta


class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offers"
    
    price = fields.Float('Price')
    status = fields.Selection(
        string='Status',
        copy=False,
        selection = [('accepted', "Accepted"), ('refused', 'Refused')]
    )
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    property_id = fields.Many2one('estate.property', string='Property', required=True)
    
    create_date = fields.Date('Creation Date', default=fields.Date.today())
    validity = fields.Integer('Validity (days)', default=7)
    date_deadline = fields.Date('Deadline', compute="_compute_date_deadline", inverse="_reverse_date_deadline")
    
    
    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = record.create_date + relativedelta(days=record.validity)
    
    def _reverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date).days