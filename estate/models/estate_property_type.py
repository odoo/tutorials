from odoo import models, fields

class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Real Estate Property Types'

    name = fields.Char(required=True, trim=True)
    property_ids = fields.One2many(comodel_name='estate.property', inverse_name='property_type_id')
    
    _sql_constraints = [
        ('unique_name', 'UNIQUE(name)', 'Property type name must be unique!'),
    ]
    