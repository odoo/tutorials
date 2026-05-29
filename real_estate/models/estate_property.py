from odoo import fields, models


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "real estate property module"

    name = fields.Char(string="Property Name")
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postal Code")
    date_availability = fields.Date(
        string="Available From", default=lambda self: fields.Date.today()
    )
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price", required=True)
    bedrooms = fields.Integer(string="Bedroom Count")
    living_area = fields.Integer(string="Living Area Count")
    facades = fields.Integer(string="Facades Count")
    has_garage = fields.Boolean(string="Has any Garage ?")
    has_garden = fields.Boolean(string="Has any Garden ?")
    garden_area = fields.Integer(string="Garden Area in (sq meter)")
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
    )
    active = fields.Boolean(string="Field Activity Status", default=True)
    state = fields.Selection(
        string="Property State",
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        default="new",
        required=True,
    )
    property_type_id = fields.Many2one(
        "estate.property.type",
        string="Property Type",
    )
    buyer_id = fields.Many2one(
        "res.partner",
        string="Buyer",
        copy=False,
    )
    salesman_id = fields.Many2one(
        "res.users",
        string="Salesperson",
        default=lambda self: self.env.user,
    )
    tag_ids = fields.Many2many(
        "estate.property.tag",
        string="Tags",
    )
