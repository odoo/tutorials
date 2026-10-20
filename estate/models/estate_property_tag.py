# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = "estate_property_tag"
    _description = "Estate Property Tag"
    _order = "sequence"

    name = fields.Char('Name', required=True, translate=True)
    description = fields.Text('Description')
    active = fields.Boolean('Active', default=True)
    sequence = fields.Integer('Sequence', default=10)

