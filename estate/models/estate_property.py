from odoo import fields, models
from datetime import timedelta  # Import timedelta

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"

    name = fields.Char(required=True)
    # active field define here
    active = fields.Boolean(string="Active",default=True)
    description = fields.Text()
    postcode = fields.Char()
    
    # Setup the default availability date to 3 months from current date
    date_availability = fields.Date(string="Availability Date", copy=False, default=lambda self: fields.Date.today() + timedelta(days=90))
    
    expected_price = fields.Float(required=True)
    
    # Making SP readonly and preventing it from being copied
    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False)
    
    # Making Default number of bedrooms set to 2
    bedrooms = fields.Integer(string="Number of Bedrooms", default=2)
    
    living_area = fields.Integer(string="Living Area(sqm)")
    facades = fields.Integer()
    
    # Boolean fields for garage and garden
    is_garage = fields.Boolean()
    is_garden = fields.Boolean()
    garden_area = fields.Integer(string="Garden(sqm)")
    
    # Selecting garden orientation from predefined options
    garden_orientation = fields.Selection([
        ('north', 'North'), #(sorted database,UI display value)
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West')
    ])
    state = fields.Selection([
        ('new','NEW'),
        ('offer received','Offer Received'),
        ('offer accepted','Offer Accepted'),
        ('sold','Sold'),
        ('cancelled','Cancelled')
    ],string='Status',default="new",copy=False)
    