from odoo import models, fields

class EstatePropertyType(models.Model):
    _name = "estate_property_type"
    _description = 'Type for categorizing estate properties'

    name = fields.Char('Name', required=True)