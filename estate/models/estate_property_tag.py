from random import randint

from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'estate property tags'
    _order = 'name'

    _name_uniq = models.Constraint(
        'unique (name)',
        'Name already exists!',
    )

    def _get_default_color(self):
        return randint(1, 11)

    name = fields.Char(required=True)
    color = fields.Integer('Color', default=_get_default_color)
