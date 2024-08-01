from odoo import fields, models
from datetime import datetime, timedelta

class Estateproperty(models.Model):
    _name = "estate.property"
    _description = "Estate Properties"
    
    name = fields.Char(required=True)
    postcode = fields.Char()
    description = fields.Text()
    Availbility_Date =  fields.Date(default=lambda self: datetime.today() + timedelta(days=90),copy = False)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(default = 10000,readonly=True,copy = False)
    bedrooms = fields.Integer(default=2 )
    living_area = fields.Float("Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Float("Garden Area (sqm)")
    garden_orientation = fields.Selection(
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')
        ],
        string="Garden Orientation"
    )
    Active = fields.Boolean(default = False)

    state = fields.Selection(selection=[
        ('New','New'),
        ('Offer Received', 'Offer Received'),
        ('Offer Accepted', 'Offer Accepted'),
        ('Sold', 'Sold'),
        ('canceled','canceled')
    ],
    required=True,
    copy=False,
    default = 'New',
    string="Status",
    )
