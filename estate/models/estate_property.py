from datetime import date
from dateutil.relativedelta import relativedelta
from odoo import fields, models


class EstateProperty(models.Model):
    _name = "estate_model"
    _description = "This is to say that this is the description of the Estate Model"

    name = fields.Char("Name", default="Unknown", required=True)
    description = fields.Text("Description")
    postcode = fields.Char("Postcode")
    date_availability = fields.Date(
        "Date Availability", copy=False, default=date.today() + relativedelta(months=3)
    )
    expected_price = fields.Float("Expected Price", required=True)
    selling_price = fields.Float("Selling Price", readonly=True)
    bedrooms = fields.Integer("Bedrooms", default=2)
    living_area = fields.Integer("Living Area(sqm)")
    facades = fields.Integer("Facades")
    garage = fields.Boolean("Garage")
    garden = fields.Boolean("Garden")
    last_seen = fields.Datetime("Last Seen", default=fields.Datetime.now)
    garden_area = fields.Integer("Garden Area")
    active = fields.Boolean("Active", default=True)
    partner_id = fields.Many2one("res.partner", string="Salesperson")
    buyer_id = fields.Many2one("res.users", string="Buyer")
    property_type_id = fields.Many2one("estate_type", string="Property Type")
    property_tag_id = fields.Many2many("estate_tags")

    offers_id = fields.One2many("estate_offer", "property_id")
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
            ("east", "East"),
            ("west", "West"),
            ("north", "North"),
            ("south", "South"),
        ],
        help="This is the direction of the proprety, which side the preperty is facing.",
    )
    state = fields.Selection(
        default="new",
        string="State",
        selection=[
            ("new", "New"),
            ("offer received", "Offer Received"),
            ("offer accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        help="This field tells the state of the property.",
    )
