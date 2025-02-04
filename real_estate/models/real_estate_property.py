from odoo import fields, models


class Properties(models.Model):
    _name = 'real.estate.property'
    _description = "Real Estate Property Table to store information."

    name = fields.Char("Property Name", required=True)
    description = fields.Text("Property Description")
    postcode = fields.Char("Postcode")
    date_availability = fields.Date(
        "Date Availability", 
        copy=False,
        default=lambda self: fields.Date.today() + relativedelta(months=3)
    )
    expected_price = fields.Float("Expected Price", required=True)
    selling_price = fields.Float("Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer("Bedrooms", default=2)
    living_area = fields.Integer("Living Area")
    facades = fields.Integer("Facades")
    garage = fields.Boolean("Garage")
    garden = fields.Boolean("Garden")
    garden_area = fields.Integer("Garden Area")
    garden_orientation = fields.Selection(
        string='Type',
        selection=[
            ('north', "North"), 
            ('south', "South"),
            ('east', "East"), 
            ('west', "West")
        ]
    )
    active = fields.Boolean(string="Active", default=True)
    state = fields.Selection(
        string='State',
        selection=[('new', "New"),
                   ('offer_received', "Offer Received"),
                   ('offer_accepted', "Offer Accepted"),
                   ('sold', "Sold"),
                   ('cancelled', "Cancelled")],
        required=True,
        default="new",
        copy=False
    )
