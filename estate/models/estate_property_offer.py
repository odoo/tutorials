# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offers"
    
    #name = fields.Char('Name', required=True, translate=True)
    price = fields.Float('Price')
    status = fields.Selection(
        string='Status',
        copy=False,
        selection = [('accepted', "Accepted"), ('refused', 'Refused')]
    )
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    property_id = fields.Many2one('estate.property', string='Property', required=True)