# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type"

    name = fields.Char(string="Property Type", required=True)

    _sql_constraints = [
        ('check_unique_property_type', 'UNIQUE(name)',
         'Property type is already exists')
    ]
