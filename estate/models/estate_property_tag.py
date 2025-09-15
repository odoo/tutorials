from odoo import models, fields
from random import randint


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate property tags"
    _order = "name"

    def _get_default_color(self):
        return randint(1, 11)

    name = fields.Char("Name", required=True)
    color = fields.Integer(
        string="Color",
        default=_get_default_color,
        aggregator=False,
    )

    _name_unique = models.Constraint("unique (name)", "The name must be unique")
