from odoo import models, fields
from dateutil.relativedelta import relativedelta

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "This is the model for estate property"


    name = fields.Char(string = "Name", required = True)
    description = fields.Text(string = "Description")
    postcode = fields.Char(string = "PostCode")
    date_availability = fields.Date(string = "Available From", copy=False, default=lambda self: fields.Date.today() + relativedelta(months=3))
    expected_price = fields.Float(string = "Expected Price", required = True)
    selling_price = fields.Float(string = "Selling Price", readonly= True, copy=False)
    bedrooms = fields.Integer(string = "Bedrooms", default=2)
    living_area = fields.Integer(string = "Living Area")
    facades = fields.Integer(string = "Facades")
    garage = fields.Boolean(string = "Garage")
    garden = fields.Boolean(string = "Garden")
    garden_area = fields.Integer(string = "Gardern Area")
    gardern_orientation = fields.Selection(
        string="Gardern Orientation",
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West")
        ])
    active = fields.Boolean(string = "Active", default = True)
    state = fields.Selection(
        string = "State",
        selection = [
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled")
        ],
        required = True,
        default = "new"
    )
