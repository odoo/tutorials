from odoo import fields, models
from dateutil.relativedelta import relativedelta


class Properties(models.Model):
    _name = 'real.estate.property'
    _description = "Real Estate Property Table to store information."

    # Description
    name = fields.Char("Property Name", required=True)   #Property Name
    description = fields.Text("Property Description")    #Property Description
    postcode = fields.Char("Postcode")     #Postcode  
    date_availability = fields.Date(
        "Availabile From", 
        copy=False,
        default=fields.Datetime.today() + relativedelta(months=3)
    )       #Available From

    expected_price = fields.Float("Expected Price", required=True)  #Expected Price
    selling_price = fields.Float("Selling Price", readonly=True, copy=False)    #Selling Price
    bedrooms = fields.Integer("Bedrooms", default=2)    #Bedrooms
    living_area = fields.Integer("Living Area")     #Living Area
    facades = fields.Integer("Facades")     #Facades
    garage = fields.Boolean("Garage")       #Garage
    garden = fields.Boolean("Garden")       #Garden
    garden_area = fields.Integer("Garden Area")     #Garden area
    garden_orientation = fields.Selection(  
        string='Type',
        selection=[
            ('north', "North"), 
            ('south', "South"),
            ('east', "East"), 
            ('west', "West")
        ]
    )       #Garden Orientation

    active = fields.Boolean(string="Active", default=True)      #active or not
    state = fields.Selection(
        string='State',
        selection=[('new', "New"),
                   ('offer_received', "Offer Received"),
                   ('offer_accepted', "Offer Accepted"),
                   ('sold', "Sold"),
                   ('cancelled', "Cancelled")],
        required=True,
        default="new",
        copy=False
    )       #State of property
