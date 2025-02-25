# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class EstatePropertiesTags(models.Model):
    _name = 'estate.properties.tags'
    _description = 'Estate Properties Tags'
    _order = 'name'
    _sql_constraints = [
        ('name_uniq', 'UNIQUE(name)',
         'Tag name should be unique')
    ]

    name = fields.Char(string='Name', required=True)
    color = fields.Integer(string='Sequence', default=1)
