from odoo import models, fields # type: ignore
from datetime import date
from dateutil.relativedelta import relativedelta

class property(models.Model):
    _name = 'estate.property' 
    _description = 'property'

    name = fields.Char(string="Property Name", required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(string="Available From", default=date.today()+relativedelta(months=+3), copy=False)
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Has Garage")
    garden = fields.Boolean(string="Has Garden")
    garden_area = fields.Integer(string="Garden Area (sqm)")
    
    garden_orientation = fields.Selection(
        [('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        string="Garden Orientation"
    )
    status=fields.Selection(
        [('new', 'New'),('offer_received','Offer Received'), ('offer_accepted', 'Offer Accepted'),('sold','Sold'),('cancelled','Cancelled')],
        string="Status ",
        default='new',
        copy=False
        
    )
    active = fields.Boolean(string="Active", default=True)
