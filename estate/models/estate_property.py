from odoo import models, fields
from datetime import timedelta

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Bất động Sản"

    name = fields.Char(string="Title", required=True)
    description = fields.Text(string="Description")
    postcode = fields.Integer(string="Postcode")
    date_availability = fields.Datetime(
        string="Available From",
        copy=False,
        default=lambda self: fields.Datetime.now() + timedelta(days=90),
    )
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price", readonly="1", copy=False)
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Char(string="Living Area (sqm)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage", default=True)
    garden = fields.Boolean(string="Garden", default=True)
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
        help="Type is used to separate North, South, East, West",
    )
    is_active = fields.Boolean( string="Active", default=False)
    state = fields.Selection(
        string="State",
        selection=[
            ("new", "New"),
            ("offerReceived", "Offer Received"),
            ("offerAccepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
    )
    salesman = fields.Text(string="Salesman")
    buyer = fields.Text(string="Buyer")
    property_type_id = fields.Many2one("estate.property.type", string="property type")
    buyer_id = fields.Many2one("res.partner", string = "Buyer", copy = False)
    seller_id = fields.Many2one("res.users", string = "Salesman", default = lambda self: self.env.user )
    tag_ids = fields.Many2many("estate.property.tag")
    offer_ids = fields.One2many("estate.property.offer", "property_id")
