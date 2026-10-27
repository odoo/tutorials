from random import randint

from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate property tags"
    _order = "name"

    def _get_default_color(self):
        return randint(1, 11)

    name = fields.Char("Name", required=True)
    color = fields.Integer("Color", default=_get_default_color)

    _uniq_name = models.Constraint(
        "UNIQUE(name)",
        "This name is already taken",
    )
