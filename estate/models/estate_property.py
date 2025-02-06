from odoo import fields, models
from datetime import timedelta

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property Name"

    name = fields.Char('Property name', required = True, size = 30)
    selling_price = fields.Integer('Selling Price', readonly = True, copy = False)
    description = fields.Text('Property description', size = 50)
    postcode = fields.Char('Postcode', size =6)
    date_availability = fields.Date(
        default=fields.Date.today() + timedelta(days=90), copy=False
    )
    expected_price = fields.Float('Expected price', required = True)
    bedrooms = fields.Integer('No.of bedrooms', default = 2)
    living_area = fields.Integer('Area')
    facades = fields.Integer('facade')
    garage = fields.Boolean('Available')
    garden = fields.Boolean('Present')
    garden_area = fields.Integer('Garden Area')
    active = fields.Boolean('Active',
        default = True,
        help = 'Mark if you want it as Active'
    )
    garden_orientation = fields.Selection(
        string = 'Type',
        selection = [
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')]
    )
    state = fields.Selection(
        string="State",
        required=True,
        default="new",
        copy=False,
        selection=[
            ("new", "New"),
            ("offer received", "Offer Received"),
            ("offer accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
    )
