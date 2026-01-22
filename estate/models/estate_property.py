from dateutil.relativedelta import relativedelta
from odoo import models, fields


class Property(models.Model):
    _name = "estate.property"
    _description = "Estate Property app like immoweb"

    name = fields.Char(string="Title", required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    offer_ids = fields.One2many("estate.property.offer", string="Offers", inverse_name="property_id")
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    salesman = fields.Many2one("res.users", string ="Salesman", default=lambda self: self.env.uid)
    buyer = fields.Many2one("res.partner", string="Buyer", copy=False)
    date_availability = fields.Date(string="Available From", default=fields.Date.today() + relativedelta(months=3), copy=False)
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area")
    active = fields.Boolean(string="Active", default=True)
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West")
        ]
    )
    state = fields.Selection(
        string="Status",
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled")
        ],
        default="new"
    )
