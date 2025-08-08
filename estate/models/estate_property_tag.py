# imports of odoo
from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Property tags to represent the property.'
    _order = 'name'

    # SQL Constraints
    _sql_constraints = [
        ('unique_tag_name', 'UNIQUE(name)', 'Tag name must be unique.'),
    ]

    name = fields.Char('Property Tag', required=True)
    color = fields.Integer(string="Color")
