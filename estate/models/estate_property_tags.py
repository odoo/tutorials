from odoo import models, fields, api
import random


class EstatePropertyTags(models.Model):
    _name = "estate_property_tags"
    _description = "property tags"
    _order = "name asc"

    @api.model
    def _get_random_color(self):
        return random.randint(1, 11)

    name = fields.Char(required=True)
    color = fields.Integer(default=_get_random_color)

    _sql_constraints = [
        ('check_unique_name', 'UNIQUE(name)', 'The name of the tag should be unique'),
    ]
