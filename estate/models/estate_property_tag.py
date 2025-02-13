# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Real Estate Property Tag"
    _order = "name"
    _sql_constraints = [
        ('unique_tag_name', 'UNIQUE(name)', 'property tag name must be unique.')
    ]

    name = fields.Char(string='Name', required=True)
    color = fields.Integer(string='Color')
