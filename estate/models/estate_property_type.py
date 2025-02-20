# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api


class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Types"
    _order = "sequence, name asc"
    
    _sql_constraints = [
        ('check_unique_name', 'UNIQUE(name)',
         "The name of the property type must be unique.")
    ]
    
    name = fields.Char('Name', required=True, translate=True)
    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")
    property_ids = fields.One2many('estate.property', 'property_type_id')
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id')
    offer_count = fields.Integer('Offer Count', compute="_compute_offer_count")
    
    
    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
    
    