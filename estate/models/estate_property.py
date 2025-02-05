from odoo import models, fields
from datetime import date , timedelta


class EstateProperty(models.Model):
    _name = "estate.property" 
    _description = "Real Estate Property"

    name = fields.Char(string="Title", required=True)
    expected_price = fields.Float(string="Expected Price", required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(string="Available From",copy=False,default=lambda self: date.today() + timedelta(days=(90)))
    selling_price = fields.Float(string="Selling Price",readonly=True,copy=False)
    bedrooms = fields.Integer(string="Bedrooms",default=2)
    living_area = fields.Integer(string="Living Area")
    facades = fields.Integer(string="Facades")
    active = fields.Boolean(default=True)
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area")
    garden_orientation = fields.Selection(
        [('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        string="Garden Orientation"
    )
    state = fields.Selection([
        ('new', 'New'),
        ('offer_received', 'Offer Received'),
        ('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('cancelled', 'Cancelled'),
    ], 
    string="State", required=True, default='new', copy=False 
    )

