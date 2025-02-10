from odoo import fields, models
from datetime import timedelta

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Types of Properties are stored"
    
    name = fields.Char(string="Name")
    description = fields.Char(string="Description")
    property_type = fields.Selection(
        string = 'Property Type',
        required = True,
        default = 'house',
        selection = [
            ('house', 'House'),
            ('appartment', 'Appartment'),
            ('penthouse', 'Pent-House'),
            ('bunglow', 'Bunglow'),
            ('castle', 'Castle')
        ],
    )
    postcode = fields.Char('Postcode', size =6)
    date_availability = fields.Date(
        default=fields.Date.today() + timedelta(days=90), copy=False
    )
    selling_price = fields.Integer('Selling Price',
        readonly = True,
        copy = False,
        default = 1000000
    )
    expected_price = fields.Float('Expected price', required = True)