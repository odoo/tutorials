# -*- coding: utf-8 -*-
from odoo import models, fields

class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Real Estate Property Tag'
    _order = 'name'

    name = fields.Char(required=True, copy=False)
    color = fields.Integer(string='Color Index', help="Color index for UI representation.")

    _sql_constraints = [
        ('unique_property_tag_name', 'UNIQUE(name)', 'The property tag name must be unique!')
    ]
