from random import randint
from odoo import models, fields


class PropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = "Property tag"

    _sql_constraints = [
        ('check_unique_name', 'UNIQUE(name)', "This tag name already exists."),
    ]
    _order = "name asc"

    name = fields.Char("Name", required=True)
    color = fields.Integer("Color", default=lambda _: randint(1, 10))
