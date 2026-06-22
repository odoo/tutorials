from odoo import models,fields

class EstatePropertyType(models.Model):
    _name= "estate.property.type"
    _description = "model for estate property types"
    name= fields.Char(required=True)
    
    

    