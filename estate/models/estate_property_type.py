from odoo import models, fields

class EstatePropertyType(models.Model):
    _name = 'estate.property.type'

    _sql_constraints = [
        ('unique_type_name', 'UNIQUE(name)', 'Property type name must be unique.'),
        ]
    
    _description = 'Property Type'

    name = fields.Char(required=True)
    property_id = fields.One2many(
        'estate.property',
        'property_type_id',
        string="Property"
    )