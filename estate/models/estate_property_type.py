# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type"
    _order = "sequence, name, id"
    _sql_constraints = [
        ("check_name", "UNIQUE(name)", "The name must be unique"),
    ]

    name = fields.Char("Name", required=True)
    sequence = fields.Integer("Sequence")

    property_ids = fields.One2many("estate.property", "property_type_id", string="Properties")
