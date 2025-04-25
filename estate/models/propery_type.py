# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class PropertyType(models.Model):
    _name = "property_type"
    _description = "Property Types"
    name = fields.Char(required=True)

    _sql_constraints = [
        (
            "unique_type_name",
            "UNIQUE(name)",
            "Property type must be unique.",
        ),
    ]
