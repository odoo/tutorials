from odoo import models,fields

class PropertyType(models.Model):
    
    _name = "estate_property_type"
    _description = "The type of the real estate property i.e. house, apartment, etc"
    name = fields.Char(required = True)