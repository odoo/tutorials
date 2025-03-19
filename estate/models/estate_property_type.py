from odoo import fields, models


class PropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Real estate property type'

    name = fields.Char(required=True)
    property_ids = fields.One2many('estate.property','property_type_id')

    _sql_constraints = [
        ('unique_property_type', 'unique(name)', 'Property type must be unique'),
    ]
