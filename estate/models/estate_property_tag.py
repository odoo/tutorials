import random

from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Estate property tags'

    def _get_default_color(self):
        return random.randint(1, 11)

    name = fields.Char(required=True)
    color = fields.Integer(default=_get_default_color)
