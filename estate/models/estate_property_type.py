from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate property type model'

    name = fields.Char(string='Title', required=True)

    _sql_constraints = [
        ('unique_property_type', 'UNIQUE(name)', 'Property type must be unique.')
    ]
