from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Estate property Tag'
    _order = 'name'

    name = fields.Char(string='Name')
    color = fields.Integer(string='Color')

    _sql_constraints = [
        ('check_name', 'UNIQUE(name)', 'A tag must be unique.'),
    ]
