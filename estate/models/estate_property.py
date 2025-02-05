from odoo import models, fields
from datetime import datetime
from dateutil.relativedelta import relativedelta

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"

    def calculate_three_months_later():
        today = datetime.now()

        return today + relativedelta(months=3)

    # Fields of Property
    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(string="Date Availability", default=calculate_three_months_later(), copy=False)
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area")
    
    # Garden Orientation of Property
    garden_orientation = fields.Selection(
        string="Garden Orientation", 
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')]);
    
    active = fields.Boolean(string="Is Active", default=True)
    
    # State Selection of Property
    state = fields.Selection(
        string="State", 
        required=True, 
        copy=False,
        default="new",
        selection=[('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'), ('cancelled', 'Cancelled')])