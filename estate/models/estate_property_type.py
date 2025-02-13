# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type"
    _order = 'sequence asc'
    sequence = fields.Integer(string="Sequence", default=10)

    name = fields.Char(string="Property Type", required=True)
    property_ids = fields.One2many("estate.property", "property_type_id", string="Properties")

    _sql_constraints = [
        ('check_unique_property_type', 'UNIQUE(name)',
         'Property type is already exists')
    ]
