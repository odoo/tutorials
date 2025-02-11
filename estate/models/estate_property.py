from odoo import api, fields, models
from datetime import datetime, timedelta


class EstateProperty(models.Model):

    _name = "estate.property"
    _description = "Declare property for Real estate"

    # --------------------------------------- Fields Declaration ----------------------------------
    name = fields.Char(required=True)
    description = fields.Text("Description")
    postcode = fields.Char("Postcode")
    date_availability = fields.Date(
        "Available From", default=datetime.now() + timedelta(90)
    )
    expected_price = fields.Float("Expected Price", required=True)
    selling_price = fields.Float("Selling Price", copy=False, readonly=True)
    bedrooms = fields.Integer("Bedrooms", default="2")
    living_area = fields.Integer("Living Area (sqm)")
    facades = fields.Integer("Facades")
    is_garage = fields.Boolean("Garage")
    is_garden = fields.Boolean("Garden")
    garden_area = fields.Integer("Garden Area (yard)")
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
        help="Choose the orientation of a garden from the options: North, South, East, or West.",
    )
    state = fields.Selection(
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        string="Status",
        required=True,
        copy=False,
        default="new",
    )
    active = fields.Boolean("Active", default=True)
    # Relational
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    user_id = fields.Many2one(
        "res.users", string="Salesman", default=lambda self: self.env.user
    )
    buyer_id = fields.Many2one("res.partner", string="Buyer", readonly=True, copy=False)
    # Relational Field for tag's (Many2Many)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    # Relation Field for offer (one2Many)
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    total_area = fields.Float(string="Total Area (sqm)", compute="_compute_total_area")
    best_price = fields.Float(
        string="Best Offer", compute="_compute_best_price", help="Best offer so far."
    )

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        # breakpoint()
        for value in self:
            value.total_area = value.living_area + value.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        # breakpoint()
        for value in self:
            if value.offer_ids:
                value.best_price = max(value.mapped("offer_ids.price"))
            else:
                value.best_price = 0.00

    @api.onchange("is_garden")
    def _onchange_garden(self):
        if self.is_garden:
            self.garden_area = 20
            self.garden_orientation = "south"
        else:
            self.garden_area = 0
            self.garden_orientation = False
