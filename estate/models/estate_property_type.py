# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = "estate_property_type"
    _description = "Estate Property Type"
    _order = "sequence"

    name = fields.Char('Name', required=True, translate=True)
    description = fields.Text('Description')
    active = fields.Boolean('Active', default=True)
    sequence = fields.Integer('Sequence', default=10)

