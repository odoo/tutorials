from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Type of Real Estate Property'

    _unique_name = models.Constraint('UNIQUE(name)', 'The name of a type should be unique.')

    name = fields.Char(required=True)
