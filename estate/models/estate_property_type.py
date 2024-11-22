from odoo import fields, models

class estate_property_type(models.Model):
    _name = "estate.property.type"  
    _description = "real estate property types"
    property_type = fields.Text()
    name = fields.Char(required=True)