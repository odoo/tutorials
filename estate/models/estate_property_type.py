from odoo import models, fields


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate Property Types'
    _order = 'name'

    _sql_constraints = [
        ('check_name', 'UNIQUE(name)',
         'The property type name must be unique')
    ]

    name = fields.Char(required = True )
    property_ids = fields.One2many('estate.property', 'property_type_id')
    sequence = fields.Integer()