from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate property type model'
    _order = 'name'

    name = fields.Char(string='Title', required=True)
    property_ids = fields.One2many('estate.property', 'property_type_id', string='Properties')
    sequence = fields.Integer('Sequence')

    _sql_constraints = [
        ('unique_property_type', 'UNIQUE(name)', 'Property type must be unique.')
    ]
