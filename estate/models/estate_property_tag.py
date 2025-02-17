# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Estate Property'
    _order = 'name asc'
    _sql_constraints = [
        ('unique_tag_name', 'UNIQUE(name)',
         'The property tag name must be unique.'),
    ]

    name = fields.Char(string='Tags', required=True)
    color = fields.Integer()
