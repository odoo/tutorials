from random import randint

from odoo import fields, models  # ty: ignore[unresolved-import]


class PropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Tag of real estate property"
    _order = "name"

    name = fields.Char(required=True)
    _check_name = models.Constraint("UNIQUE(name)", "Tag names must be unique")
    color = fields.Integer(default=lambda _: randint(1, 11))
