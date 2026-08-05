from random import randint

from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Real Estate Property Tag"
    _rec_name = 'name'
    _order = "name"

    def _default_color(self):
        return randint(1, 11)

    name = fields.Char(required=True, translate=True)
    description = fields.Char(required=True, translate=True)
    color = fields.Integer(
        string='Color Index',
        default=lambda self: self._default_color(),
    )

    _unique_name = models.Constraint("UNIQUE(name)", "The name of the tag must be unique.")
