from odoo import fields, models

class EstatePropertyType(models.Model):

    _name = 'estate.property.tag'
    _description = 'Real Estate Property Tag'

    name = fields.Char(
        string='property Type',
        required=True
    )
