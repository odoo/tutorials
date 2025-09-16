from odoo import fields, models

class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property Type"

    name = fields.Char(required=True)
    property_ids = fields.One2many('estate.property', 'property_type_id')

    _name_unique = models.Constraint('UNIQUE(name)', 'The property type name must be unique.')
