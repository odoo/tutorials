# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type"
    _sql_constraints = [
        ("unique_type_name", "UNIQUE(name)", "Property type name must be unique."),
    ]

    name = fields.Char(string="Property Type", required=True)
