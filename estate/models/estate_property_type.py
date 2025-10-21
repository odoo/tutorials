from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "test description"
    
    name = fields.Char('Name', required=True)
