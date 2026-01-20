from odoo import models, fields, api


class PropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'estate property type'
    _order = 'name'

    name = fields.Char(required=True)
    sequence = fields.Integer('Sequence', default=1, help="Used to order property types")
    property_ids = fields.One2many('estate.property', 'property_type_id', string="Properties")