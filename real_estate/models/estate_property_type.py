from odoo import fields, models

class EstatePropertyType(models.Model):

    _name = 'estate.property.type'
    _description = 'Detail About Perticular Property'

    name = fields.Char(
        string='property Type',
        required=True
    )
