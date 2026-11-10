from random import randint

from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Real estate property tags"
    _order = "name asc"

    def _default_color(self):
        return randint(1, 11)

    name = fields.Char(required=True)
    color = fields.Integer(default=lambda self: self._default_color())

    _unique_name = models.Constraint(
        "Unique(name)", "The property tag must have a unique name"
    )
