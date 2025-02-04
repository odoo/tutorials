from odoo import fields, models
from datetime import timedelta

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real estate property details"

    # Basic fields
    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description", required=True)
    postcode = fields.Char(string="Postcode")
    
    # Availability Date with default value set to 3 months from today
    def _default_availability_date(self):
        return fields.Date.today() + timedelta(days=90)

    date_availability = fields.Date(
        string="Date Availability", 
        default=_default_availability_date,  # Default to 3 months ahead
        copy=False  # Don't copy when duplicating
    )

    # Expected price
    expected_price = fields.Float(string="Expected Price")

    # Selling price - read-only and won't be copied
    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False)

    # Bedrooms with a default value of 2
    bedrooms = fields.Integer(string="Bedrooms", default=2)

    # Living area (integer) and other property features
    living_area = fields.Integer(string="Living Area")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area")
    
    # Garden Orientation - dropdown selection
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[("north", "North"), ("south", "South"), ("east", "East"), ("west", "West")]
    )

    # Reserved fields
    active = fields.Boolean(default=True)  # Active field (default True)
    
    # State field with preset states
    state = fields.Selection(
        string="State",
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled'),
        ],
        default='new',  # Default state is 'new'
        required=True,
        copy=False  # Don't copy the state when duplicating
    )
