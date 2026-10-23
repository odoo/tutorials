# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class PropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate property tag info"

    name = fields.Char(required=True)

    _unique_name = models.Constraint(
        "UNIQUE(name)",
    )
