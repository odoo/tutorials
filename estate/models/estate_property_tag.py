from random import randint

from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Real Estate Property Tag"
    _rec_name = 'name'

    def _default_color(self):
        return randint(1, 11)

    name = fields.Char(required=True)
    description = fields.Char(required=True)
    color = fields.Integer(
        string='Color Index',
        default=lambda self: self._default_color(),
    )
