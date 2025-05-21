from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'estate property type module'

    name = fields.Char(required=True)

    _sql_constraints = [
        ('unique_property_type', 'UNIQUE(name)',
         'The property type must be unique'),
    ]
