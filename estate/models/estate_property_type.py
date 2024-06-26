from odoo import models, fields

class PropertyType(models.Model):
    # Model Property
    _name = "estate.property.type"
    _description = "Estate App Property Types"
    
    # Fields
    name = fields.Char(required = True)