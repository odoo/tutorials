from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'The type of an estate property (Flat, House, Mansion)'

    name = fields.Char(required=True)
