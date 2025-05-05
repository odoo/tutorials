from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    _order = "id desc"

    name = fields.Char("Property Name", required=True)
    description = fields.Text("Description")
    postcode = fields.Char("Postcode")
    date_availability = fields.Date(
        "Availability Date",
        copy=False,
        default=lambda self: fields.Date.add(fields.Date.today(), months=3),
    )
    expected_price = fields.Float("Expected Price", required=True)
    selling_price = fields.Float("Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer("Number of Bedrooms", default=2)
    living_area = fields.Float("Living Area")
    total_area = fields.Float(string="Total Area", compute="_compute_total_area")
    facades = fields.Integer("Number of Facades")
    garage = fields.Boolean("Has Garage")
    garden = fields.Boolean("Has Garden")
    garden_area = fields.Float("Garden Area")
    garden_orientation = fields.Selection(
        [("north", "North"), ("south", "South"), ("east", "East"), ("west", "West")],
        "Garden Orientation",
    )
    active = fields.Boolean(default=True)  # <-- Reserved field: "active"

    state = fields.Selection(
        [  # <-- Reserved field: "state"
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        required=True,
        copy=False,
        default="new",
    )

    # Relationships to other models
    property_type_id = fields.Many2one(
        "estate.property.type",
        string="Property Type",
        help="Select the property type for this estate property",
    )

    buyer_id = fields.Many2one(
        "res.partner", string="Buyer", help="The buyer of this property"
    )

    salesperson_id = fields.Many2one(
        "res.users",
        string="Salesperson",
        default=lambda self: self.env.user,  # Default value is current user
        help="The salesperson handling this property",
    )

    tag_ids = fields.Many2many(
        "estate.property.tag",
        "estate_property_tag_rel",
        "property_id",
        "tag_id",
        string="Tags",
        help="Tags related to the estate property",
    )

    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    best_price = fields.Float(string="Best Offer", compute="_compute_best_price")

    property_id = fields.Many2one("estate.property")

    create_uid = fields.Many2one("res.users", string="Created by", readonly=True)
    write_uid = fields.Many2one("res.users", string="Last Updated by", readonly=True)
    create_date = fields.Datetime(string="Creation Date", readonly=True)
    write_date = fields.Datetime(string="Last Update Date", readonly=True)

    # Constraints
    _sql_constraints = [
        (
            "check_expected_price_positive",
            "CHECK(expected_price >= 0)",
            "The expected price must be strictly positive.",
        ),
        (
            "check_selling_price_positive",
            "CHECK(selling_price >= 0)",
            "The selling price must be positive.",
        ),
    ]

    # It will not be possible to accept an offer lower than 90% of the expected price.
    @api.constrains("expected_price", "selling_price")
    def _check_offer_min(self):
        for record in self:
            if float_is_zero(record.selling_price, precision_digits=2):
                continue
            min_allowed_price = record.expected_price * 0.9
            if (
                float_compare(
                    record.selling_price, min_allowed_price, precision_digits=2
                )
                < 0
            ):
                raise ValidationError(
                    "The selling price cannot be lower than 90% of the expected price."
                )

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            prices = record.offer_ids.mapped("price")
            record.best_price = max(prices) if prices else 0.0

    # show the sold price only if sold
    display_selling_price = fields.Char(
        string="Displayed Price",
        compute="_compute_display_selling_price",
        store=False,
    )

    @api.depends("selling_price", "state")
    def _compute_display_selling_price(self):
        for record in self:
            if record.state == "sold":
                record.display_selling_price = f"${record.selling_price:,.2f}"
            else:
                record.display_selling_price = "N/A"

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    # Buttons
    def action_cancel(self):
        for record in self:
            if record.state == "sold":
                raise UserError("Sold properties cannot be cancelled.")
            record.state = "cancelled"

    def action_sold(self):
        for record in self:
            if record.state == "cancelled":
                raise UserError("Cancelled properties cannot be sold.")
            record.state = "sold"

    # CRUD Functions

    @api.ondelete(at_uninstall=False)
    def _unlink_if_allowed(self):
        for record in self:
            if record.state not in ["new", "Cancelled"]:
                raise UserError(
                    "You can only delete properties in state 'New' or 'Cancelled'."
                )
