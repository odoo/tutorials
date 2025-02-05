from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta

from odoo import models, fields

class EstateProperty(models.Model):

    

    _name = "estate.property"
    _description = "Estate Property Model"

    name = fields.Char(string="Your name", required=True, default="Unknown")
    active = fields.Boolean(default=False)
    state = fields.Selection(selection = [('New', 'New'), ('Offer Received', 'Offer Received'), ('Offer Accepted', 'Offer Accepted'), ('Sold', 'Sold'), ('Cancelled', 'Cancelled')], default="New")
    last_seen = fields.Datetime("Last Seen", default=fields.Datetime.now)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=fields.Date.today() + timedelta(days=+90))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False) 
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        string="Garden Orientation",
        help="Orientation of the garden"
    )   