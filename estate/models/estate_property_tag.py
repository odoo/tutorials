from random import randint

from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Tag for categorizing estate properties'
    _order = 'name asc'

    _sql_constraints = [
        ('unique_name', 'UNIQUE(name)', 'Tag name must be unique!'),
    ]

    def _get_default_color(self):
        return randint(1, 11)

    name = fields.Char('Name', required=True)
    color = fields.Integer('Color', default=_get_default_color)
