from odoo import fields,models

class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'real estate property type'

    name= fields.Char(required=True)

    _sql_constraints = [('check_unique_name', 'UNIQUE(name)', 'Property type name must be unique.')]
