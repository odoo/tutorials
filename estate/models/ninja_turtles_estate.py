from odoo import models, fields
from datetime import date, timedelta

class NinjaTurtlesEstateModel(models.Model):
    _name = "ninja.turtles.estate"
    _description = "For the fastest progress ever!"
    
    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")

    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(
        string="Available From",
        copy=False,
        default = lambda self: date.today() + timedelta(days=90),
    )

    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(
        string="Selling Price",
        readonly=True,
        copy=False,
    )

    bedrooms = fields.Integer(
        string="Bedrooms",
        default = 2,
    )
    living_area = fields.Integer(string="Living Area (sqm)")

    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")

    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area (sqm)")

    garden_orientation = fields.Selection(
        string="Garden Orientation",		
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')
        ],
        help="Garden Orientation is for choosing your specified area for your garden."
    )
    status = fields.Selection(
        string="Status",
        selection=[
            ('new', 'New'),
            ('offer received', 'Offer Received'),
            ('offer accepted', 'Offer Accepted'),
            ('sold', "Sold"),
            ('cancelled', "Cancelled")
        ],
        required=True,
        default="new",
        copy=False
    )
    active = fields.Boolean(
        string="Active",
        default = True,
    )

    property_type_id = fields.Many2one(
        "ninja.turtles.estate.property.type",
        string="Property Type"
    )

    buyer_id = fields.Many2one(
        "res.partner",
        string="Buyer",
        copy=False
    )

    salesperson_id = fields.Many2one(
        "res.users",
        string="Salesperson",
        default=lambda self: self.env.user
    )

    tag_ids = fields.Many2many(
        "ninja.turtles.estate.property.tag",
        string="Tags"
    )



