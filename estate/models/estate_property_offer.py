# -- coding: utf-8 --
# Part of Odoo. See LICENSE file for full copyright and licensing details. 

from odoo import models, fields

class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Property Offer'

    price = fields.Float('Offer Price')
    status = fields.Selection([
                               ('accepted', 'Accepted'),
                               ('refused', 'Refused')], string='Status', default='refused')
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    property_id = fields.Many2one('estate.property', string='Property', required=True)


