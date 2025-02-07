from odoo import fields, models

class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Stores types of Property"
    
    name = fields.Char('Name', required=True)
