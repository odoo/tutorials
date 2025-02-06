from datetime import timedelta

from odoo import models, fields


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property Model"

    name = fields.Char(string="Name", required=True, default="Unknown")
    active = fields.Boolean(string="Active", default=True)
    state = fields.Selection(
        [('new', 'New'), 
        ('offer received', 'Offer Received'), 
        ('offer accepted', 'Offer Accepted'), 
        ('sold', 'Sold'), 
        ('cancelled', 'Cancelled')], 
        default="new",
        string="State"
    )
    last_seen = fields.Datetime(string="Last Seen", default=fields.Datetime.now)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(string="Available from", copy=False, default=fields.Date.today() + timedelta(days=+90))
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False) 
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area")
    garden_orientation = fields.Selection(
        [('north', 'North'), 
        ('south', 'South'), 
        ('east', 'East'), 
        ('west', 'West')],
        string="Garden Orientation",
        help="Orientation of the garden"
    )   
