from odoo import fields,models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property type for an estate"
    
    name = fields.Char("Name",required=True)
    

