# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Types"
    
    _sql_constraints = [
        ('check_unique_name', 'UNIQUE(name)',
         "The name of the property type must be unique.")
    ]
    
    name = fields.Char('Name', required=True, translate=True)
    property_ids = fields.One2many('estate.property', 'property_type_id')