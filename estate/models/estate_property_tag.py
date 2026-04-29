from random import randint

from odoo import fields, models


class Tag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"
    _order = "name"

    def _get_default_color(self):
        return randint(0, 11)

    name = fields.Char(string="Tag Name", required=True)
    color = fields.Integer(default=_get_default_color)

    _name_uniq = models.Constraint(
        "unique (name)",
        "Tag name must be unique",
    )
