from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "real estate property types"
    
    name = fields.Char(string = "Property Types Names")
    single = fields.Char()
    