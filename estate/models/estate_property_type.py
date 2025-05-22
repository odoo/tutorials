from odoo import fields, models


class EstateType(models.Model):
    _name = 'estate.property.type'
    _description = 'It allows to create a new property type'
    _order = 'sequence desc'

    name = fields.Char(required=True)
    sequence = fields.Integer('Sequence', default=1, help='Used to order properties types. Lower is better.')
    properties_ids = fields.One2many('estate.property', 'property_type_id')
