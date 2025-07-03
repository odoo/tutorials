from odoo import models, fields

class RealEstate(models.Model):
    _name = "real.estate"
    _description = "This is a real estate module"
    
    
    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date()
    expected_price = fields.Float(required=True)
    selling_price  = fields.Float()
    bedrooms  = fields.Integer()
    living_area  = fields.Integer()
    facades  = fields.Integer()
    garage  = fields.Boolean()
    garden  = fields.Boolean()
    garden_area  = fields.Integer()
    garden_orientation = fields.Selection(
        selection=[
            ('north','North'),
            ('south','South'),
            ('east','East'),
            ('west','West')
            ]
        )