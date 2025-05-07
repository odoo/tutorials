from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type"
    
    # Basic Fields
    name = fields.Char(required=True)
    