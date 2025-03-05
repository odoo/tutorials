from odoo import models, fields # type: ignore
from datetime import datetime
from dateutil.relativedelta import relativedelta

class RealEstateProperty(models.Model):
    _name = 'estate.property'  # Database table name
    _description = 'Real Estate Property'

    name = fields.Char(string="Property Name", required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(string="Available From" , copy=False , default=datetime.today() + relativedelta(months=3))
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer(string="Bedrooms", default="2")
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Has Garage")
    garden = fields.Boolean(string="Has Garden")
    garden_area = fields.Integer(string="Garden Area (sqm)")
    
    garden_orientation = fields.Selection(
        [('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        string="Garden Orientation"
    )

    state = fields.Selection(
        [('new' , "New"), ('offer_received','Offer Received'), ('offer_accepted','Offer Accepted'), ('sold','Sold'), ('cancelled','Cancelled')],
        string="State" ,
        default="new",
        copy=False,
        required=True,
    )
    garden = fields.Boolean(string="Active")
