from odoo import models, fields


class PropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Defines the property type: house, apartment, penthouse, castle, etc.'

    name = fields.Char('Name', required=True)
