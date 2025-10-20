from odoo import models, fields 

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"

    name = fields.Char(string="Title", required=True)
    expected_price = fields.Float(required=True)
    bedrooms = field.Integer(default=2)
    
