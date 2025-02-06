from odoo import fields, models
from datetime import timedelta

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property Name"

    name = fields.Char('Property Name', required=True, size=30)
    description = fields.Text('Description', size=50)
    postcode = fields.Char('Postcode', size=6)
    date_availability = fields.Date('Date Availability',default=fields.Date.today() + timedelta(days=90), copy=False)
    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float('Selling Price', readonly=True, copy=False)
    bedrooms = fields.Integer('Bedrooms', default="2")
    living_area = fields.Integer('Living Area')
    facades = fields.Integer('Facedes')
    garage = fields.Integer('Garage')
    garden_area = fields.Integer('Garden Area')
    garden_orientation = fields.Selection(
        string ='Type',
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')    
        ]
    )
    active = fields.Boolean('Active', 
        default=True, 
        help='if you wan to active'
        )
    state = fields.Selection(
        required=True,
        copy=False,
        default="new",
        selection=[
            ('new', 'New'),
            ('offer received', 'Offer Received'),
            ('offer accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled')
        ]
    )
