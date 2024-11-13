from odoo import models, fields                     

class EstatePropertyType(models.Model):
    _name = "estate.property.types"
    _description = "Real Estate Property Type"
    
    name = fields.Char(required=True,string="Property Type")
