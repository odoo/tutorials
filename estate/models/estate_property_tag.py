from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'A property tag'
    _order = 'name'

    name = fields.Char(string='Name', required=True)
    color = fields.Integer(string='Color')

    _sql_constraints = [
        ('unique_name',
         'UNIQUE(name)',
         'Property tags must be unique')
    ]
