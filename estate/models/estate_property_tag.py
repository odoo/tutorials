from odoo import models, fields

class EstatePropertyTags(models.Model):
    _name = "estate.property.tags"
    _description = "Real Estate Property tags"
    
    name = fields.Char(required=True,string="Property tags")
