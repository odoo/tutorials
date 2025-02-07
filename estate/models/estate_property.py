from datetime import datetime
from odoo import fields, models
from dateutil.relativedelta import relativedelta


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"

    active = fields.Boolean(string="Active", default=True)

    name = fields.Char(required=True)
    description = fields.Text("Description")
    postcode = fields.Text(string="Postcode")
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price")
    bedrooms = fields.Integer(string="Number of Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area (m²)")
    facades = fields.Integer(string="Number of Facades")
    garage = fields.Boolean(string="Has Garage")
    garden = fields.Boolean(string="Has Garden")
    garden_area = fields.Integer(string="Garden Area (m²)")
    date_availability = fields.Date(
        string="Date Availability", default=datetime.today() + relativedelta(months=3)
    )
    status = fields.Selection(
        [
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        string="State",
        default="new",
        required=True,
        copy=False,
    )

    garden_orientation = fields.Selection(
        [
            ("north", "North"),
            ("east", "East"),
            ("west", "West"),
            ("south", "South"),
        ],
        string="Garden Orientation",
        default="north",
    )

    property_type_id = fields.Many2one("property.type", string ="Property Type")
    tags_ids=fields.Many2many("property.tag", string="Property Tags")
    buyer_id = fields.Many2one("res.partner", string ="Buyer")
    seller_id = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.user)
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string="Offer Id")
