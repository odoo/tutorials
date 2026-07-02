from odoo import fields,models  


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"
    
    name = fields.Char()
    expected_price = fields.Float()
    bedrooms = fields.Integer()