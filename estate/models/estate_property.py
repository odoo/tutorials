from odoo import models,fields
from dateutil.relativedelta import relativedelta

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"
    
    name = fields.Char("Property Name", required=True)
    description = fields.Text("Description")
    postcode = fields.Char("Postcode")
    date_availability = fields.Date("Available From", copy=False, default=fields.Date.today() + relativedelta(months=3))
    expected_price = fields.Float("Expected Price")
    selling_price = fields.Float("Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer("Bedrooms", default=2)
    living_area = fields.Integer("Living Area (sqm)")
    facades = fields.Integer("Facades")
    garage = fields.Boolean("Garage")
    garden = fields.Boolean("Garden")
    garden_area = fields.Integer("Garden Area (sqm)")
    active = fields.Boolean(default=True)
    garden_orientation = fields.Selection( 
        string="Garden Orientation",
        selection=[
            ('north', 'North'), 
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West'),
        ]
    )
    state = fields.Selection(
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled'),
        ],
        required=True, copy=False, default='new',
    )
