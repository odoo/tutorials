from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'A property type'

    name = fields.Char('Name', required=True)

    _sql_constraints = [
        ('unique_name',
         'UNIQUE(name)',
         'Property types must be unique.')
    ]
