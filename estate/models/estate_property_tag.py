# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = "Property Tag"
    _order = "name"

    name = fields.Char(required=True, string="Property Tag")
    color = fields.Integer()

    _unique_tag = models.Constraint(
        "UNIQUE(name)", "The tag must be unique"
    )
