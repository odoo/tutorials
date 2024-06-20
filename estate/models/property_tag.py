# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models

class PropertyTag(models.Model):
    _name = "property.tag"
    _description = "Property tags of a Real Estate"
    _order = "name"

    name = fields.Char(required=True)
    color = fields.Integer()

    _sql_constraints  = [
        ('check_unique_tag', 'unique (name)', 'Odoopsie! This name is already chosen' )
    ]