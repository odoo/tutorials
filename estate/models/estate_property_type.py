# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'Property type name must be unique!')
    ]

    name = fields.Char(string='Property Type', required=True)
