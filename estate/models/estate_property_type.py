from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Define type of properties'

    name = fields.Char(required=True)
    