from odoo import fields, models
from datetime import datetime, timedelta

class Property_Plan(models.Model):
    _name = "estate_property"
    _description = "Test Model"
    name = fields.Char(string="Title",required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(string="Date Availability", copy=False, default=lambda self: (datetime.today() + timedelta(days=90)).date())
    expected_price = fields.Float(string="Expected Price",required=True)
    selling_price = fields.Float(string="Selling Price",readonly=True,copy=False)
    bedrooms = fields.Integer(string="Bedrooms",default=2)
    living_area = fields.Integer(string="Living Area")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area")
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[("north","North"), ("south","South"),("east","East"),("west","West")],
        help="Type is used for direction"
    )
    
    state = fields.Selection(string="State", selection=[('new', 'New'), ('offer received', 'Offer Received'), ('offer accepted', 'Offer Accepted'), ('sold', 'Sold'), ('cancelled', 'Cancelled')], required=True, copy=False)
    active = fields.Boolean(string="Active", default=True)
    