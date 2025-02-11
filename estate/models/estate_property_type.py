from odoo import models, fields


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate property type'
    _order = 'name'

    name = fields.Char(required=True)
    sequence = fields.Integer(string='Sequence', default=1)
    property_ids = fields.One2many('estate.property', 'property_type_id', string='Property')

    _sql_constraints = [('name_uniq', 'unique(name)', 'The name must be unique')]
