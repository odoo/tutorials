from odoo import models, fields

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property Type"
    
    name = fields.Char(required=True, string="Type", unique=True)
