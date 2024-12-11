from odoo import models, fields

class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Real Estate Property Types'
    _order = 'name'

    name = fields.Char(required=True, trim=True)
    sequence = fields.Integer(default=1)
    property_ids = fields.One2many(comodel_name='estate.property', inverse_name='property_type_id')

    _sql_constraints = [
        ('unique_name', 'UNIQUE(name)', 'Property type name must be unique!'),
    ]
