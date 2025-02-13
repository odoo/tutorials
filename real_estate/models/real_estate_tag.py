import random

from odoo import fields, models


class RealEstateTag(models.Model):
    _name = 'real.estate.tag'
    _description = "Real Estate Tag"
    _sql_constraints = [
        ('unique_name', 'unique(name)', "A property tag name must be unique.")
    ]

    def _default_color(self):
        return random.randint(1, 11)

    name = fields.Char(string="Label", required=True)
    color = fields.Integer(string="Color", default=_default_color)
