# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models

class EstatePropertyType(models.Model):
    _name="estate.property.type"
    _description = "Estate Propert Type"
    _order = "name asc"
    
    name=fields.Char("Name", required=True)
    property_ids = fields.One2many('estate.property', 'property_type_id')
    sequence = fields.Integer(string="Sequence", default=1)
    offer_ids=fields.One2many('estate.property.offer', 'property_type_id', string="Offers")
    offer_count = fields.Integer(string="Offer Count", compute="_compute_offer_count", store=True)
    
    _sql_constraints=[
        ("check_type_name", "UNIQUE(name)", "Please add differant type name")
    ]
    
    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for rec in self:
            rec.offer_count = len(rec.offer_ids)
