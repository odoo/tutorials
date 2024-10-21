from odoo import models, fields


class PropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Property Tag'
    _sql_constraints = [
        ('check_name_unique', 'UNIQUE(name)', 'The Tag name must be unique.')
    ]
    _order = 'name asc'

    name = fields.Char(string='Tag', required=True)
    color = fields.Integer(string='Color')
