from odoo import fields, models
from odoo.tools import date_utils

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate property"

    name = fields.Char(string='Estate Name', required=True)
    description = fields.Text(string='Description')
    postcode = fields.Char(string='Postcode')
    date_available = fields.Date(string='Available From Date', copy=False, default=date_utils.add(fields.Date.today(), months=3))
    expected_price = fields.Float(string='Expected Price', required=True)
    selling_price = fields.Float(string='Selling Price', readonly=True, copy=False)
    bedrooms = fields.Integer(string='Bedrooms', default=2)
    living_area = fields.Integer(string='Living Area (sqm)')
    facades = fields.Integer(string='Facades')
    garage = fields.Boolean(string='Has a Garage')
    garden = fields.Boolean(string='Has a Garden')
    garden_area = fields.Integer(string='Garden Area (sqm)')
    garden_orientation = fields.Selection(string='Garden Orientation', selection=[
        ('north', "North"),
        ('south', "South"),
        ('east', "East"),
        ('west', "West")
    ])
    active = fields.Boolean(string='Active', default=True)
    state = fields.Selection(string='State', required=True, copy=False, default='new', selection=[
        ('new', "New"),
        ('offer received', "Offer Received"),
        ('offer accepted', "Offer Accepted"),
        ('sold', "Sold"),
        ('cancelled', "Cancelled")
    ])
