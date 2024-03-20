from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'A property type'

    name = fields.Char('Name', required=True)
