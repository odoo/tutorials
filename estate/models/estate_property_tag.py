from odoo import models, fields


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Type of a property'
    _order = 'name asc'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    color = fields.Integer(string='Color')

    _sql_constraints = [
        ('Unique_name', 'unique (name)',
         'This tag name already exists'),
    ]
