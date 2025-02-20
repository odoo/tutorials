# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta


class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offers"
    _order = "price desc"
    
    _sql_constraints = [
        ('check_prices', 'CHECK(price > 0)',
         "Offer prices should be strictly positive.")
    ]
    
    price = fields.Float('Price')
    status = fields.Selection(
        string='Status',
        copy=False,
        selection = [('accepted', "Accepted"), ('refused', 'Refused')]
    )
    
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    property_id = fields.Many2one('estate.property', string='Property', required=True)
    property_type_id = fields.Many2one('estate.property.type', related='property_id.property_type_id', store=True, string='Property Type')
    property_state = fields.Selection(related="property_id.state", string="Property State")
    
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
    
    def action_accept(self):
        if self.status == 'accepted':
            raise UserError("Offer already accepted")
        elif self.status == 'refused':
            raise UserError("Can't accept a refused offer")
        else: self.property_id.action_accept_offer(self)
        
    def accept(self):
        self.status = 'accepted'
        self.property_id.selling_price = self.price
        self.property_id.buyer = self.partner_id
    
    def action_refuse(self):
        if self.status == 'refused':
            raise UserError('Offer already refused')
        if self.status == 'accepted':
            raise UserError("Can't refuse an accepted offer")
        else: self.property_id.action_refuse_offer(self)
        
    def refuse(self):
        self.status = 'refused'
    
    
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if 'property_id' in vals: 
                self.env['estate.property'].browse(vals['property_id']).state = 'offer_received'
        return super(PropertyOffer, self).create(vals_list)