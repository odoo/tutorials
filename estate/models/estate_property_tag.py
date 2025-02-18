# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Estate property tag'
    _order = 'name'

    name = fields.Char(string='Title')
    color = fields.Integer(string="Color")

    _sql_constraints = [
        ('unique_property_tag', 'UNIQUE(name)', 'Property tag must be unique.')
    ]
