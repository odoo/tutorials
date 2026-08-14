from random import randint

from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Real Estate Property Tag"
    _order = "name"

    def _default_color(self):
        return randint(1, 11)

    name = fields.Char(required=True)
    color = fields.Integer(
        string="Color Index", default=lambda self: self._default_color()
    )

    _unique_property_tag = models.Constraint(
        'UNIQUE(name)',
        'The property tag must be unique',
    )
