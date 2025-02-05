from odoo import fields, models
from dateutil.relativedelta import relativedelta
import datetime

class RealEstateProperty(models.Model):

    _name = "estate.property"
    _description = "Real Estate Property"


    # create_date = fields.Datetime(
    #     string="Creation Date", 
    #     default=datetime.datetime.now(), 
    #     readonly=True
    # )
    # create_uid = fields.Many2one(
    #     'res.users', 
    #     string='Created By', 
    #     readonly=True
    # ) 
    # write_date = fields.Datetime(
    #     string='Last Modified', 
    #     readonly=True
    # )
    # write_uid = fields.Many2one(
    #     'res.users', 
    #     string='Modified By', 
    #     readonly=True
    # )

    name = fields.Char(
        string='Property Name', 
        required=True, 
        help="Enter the name of the property"
    )
    description = fields.Text(
        string='Description', 
        required=True, 
        help="Provide a detailed description of the property"
    )
    postcode = fields.Char(
        string='Postcode', 
        required=True, 
        help="Enter the postcode of the property"
    )
    date_availability = fields.Date(
        string='Date of Availability', 
        required=True, 
        copy=False,
        default=lambda self: fields.Date.context_today(self) + relativedelta(months=+3),
        help="Specify when the property will be available"
    )
    expected_price = fields.Float(
        string='Expected Price', 
        required=True, 
        help="Enter the expected price of the property"
    )
    selling_price = fields.Float(
        string='Selling Price', 
        # required=True, 
        readonly=True,
        copy=False,
        help="Enter the selling price of the property"
    )

    bedrooms = fields.Integer(
        string='Bedrooms', 
        required=True, 
        default=2,
        help="Enter the number of bedrooms"
    )
    living_area = fields.Integer(
        string='Living Area (sq meters)', 
        required=True, 
        help="Enter the living area of the property"
    )
    facades = fields.Integer(
        string='Number of Facades', 
        required=True, 
        help="Enter the number of facades the property has"
    )
    
    garage = fields.Boolean(
        string='Has Garage', 
        help="Check if the property has a garage"
    )
    garden = fields.Boolean(
        string='Has Garden', 
        help="Check if the property has a garden"
    )
    
    
    garden_area = fields.Integer(
        string='Garden Area (sq meters)', 
        required=True, 
        help="Enter the area of the garden"
    )
    garden_orientation = fields.Selection(
        [
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')
        ],
        string='Garden Orientation',
        required=True, help="Select the orientation of the garden"
    )

    active = fields.Boolean(
        string='Active',
        default=False,
        help="If unchecked, it will archive the property."
    )

    state = fields.Selection(
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled'),
        ],
        string="State",
        required=True,
        default='new',  
        copy=False,     
        help="Current state of the property."
    )

