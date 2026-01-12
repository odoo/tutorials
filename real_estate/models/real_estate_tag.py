from random import randint

from odoo import fields, models


class RealEstateTag(models.Model):
    _name = 'real.estate.tag'
    _description = 'Real Estate Tag'
    _order = "name desc"

    def _get_default_color(self):
        return randint(1, 11)

    name = fields.Char(required=True)
    color = fields.Integer(default=_get_default_color)
    _unique_tag_name = models.Constraint(
        'UNIQUE(name)',
        'The property tag name must be unique.',
    )
