from odoo import models, fields, api


class PropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'estate property type'

    name = fields.Char(required=True)
    property_ids = fields.One2many('estate.property', 'property_type_id', string="Properties")
    