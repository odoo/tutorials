from random import randint

from odoo import fields, models


class PropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Property Tags"
    _order = "name"

    name = fields.Char(string="Name")
    color = fields.Integer(
        string='Color Index', default=lambda self: self._default_color()
    )

    _name_unique = models.Constraint(
        'UNIQUE(name)',
        'The name must be unique'
    )

    def _default_color(self):
        return randint(1, 11)
