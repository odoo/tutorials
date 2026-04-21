# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Property Tag"
    _order = "name"

    _check_name_unique = models.Constraint(
        "UNIQUE(name)", "The tag name must be unique."
    )

    name = fields.Char(required=True)
    color = fields.Integer("Color")
