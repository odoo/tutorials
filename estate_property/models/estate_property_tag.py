from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Real Estate Property Tag'

    name = fields.Char(string='Name', required=True)
    color = fields.Integer(string='Color')
    _order = 'name'
    _sql_constraints = [('name_unique', 'UNIQUE(name)', 'Property tag name must be unique')]
