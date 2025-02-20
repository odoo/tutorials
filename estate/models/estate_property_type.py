from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'the type of the property being sold'

    name = fields.Char(required = True)
