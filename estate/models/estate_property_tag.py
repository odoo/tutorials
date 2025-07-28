# imports of odoo
from odoo import fields, models


class EstatePropertyType(models.Model):
    # === Private attributes ===
    _name = 'estate.property.tag'
    _description = 'Property tags to represent the property.'
    _order = 'name'

    # SQL Constraints
    _sql_constraints = [
        ('unique_tag_name', 'UNIQUE(name)', 'Tag name must be unique.'),
    ]

    # === Fields declaration ===
    name = fields.Char('Property Tag', required=True)
    color = fields.Integer(string="Color")
