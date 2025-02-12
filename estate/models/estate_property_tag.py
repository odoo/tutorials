# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"
    _order = "name"
    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'Property tag name must be unique!')
    ]

    name = fields.Char(string='Property Tag', required=True)
    color = fields.Integer(string='Color Index', default=0)
