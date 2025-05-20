from dateutil.relativedelta import relativedelta
from odoo import fields, models


class EstateProperty(models.Model):
    _name = "estate_property"
    _description = "Estate Property"
    name = fields.Char(required = True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy = False, default=fields.Date.today() + relativedelta(months = 3))
    expected_price = fields.Float(required = True)
    selling_price = fields.Float(readonly = True, copy = False)
    bedrooms = fields.Integer(default = 2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([('North', 'north'), ('South', 'south'), ('West', 'west'), ('East', 'east')])
    state = fields.Selection([('New', 'new'), ('Offer Received', 'offer received'), ('Offer Accepted', 'offer accepted'), ('Sold', 'sold'), ('Cancelled', 'cancelled')], required = True, copy = False, default = 'New')
    active = fields.Boolean(default = True)
