from random import randint
from odoo import fields, models


class PropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Property Tag'
    _order= 'name asc'

    name = fields.Char(string="Name", required=True)
    color = fields.Integer(string="Color Index", default=lambda self: randint(1, 11))

    _sql_constraints = [
        ('uniq_name', 'unique(name)', "Property Tag Name should be unique"),
    ]
