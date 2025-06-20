from odoo import models, fields
from datetime import date, timedelta
from odoo.exceptions import UserError, ValidationError
from odoo import api
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"
    _order = "id desc"
    active = fields.Boolean(default=True)

    name = fields.Char(string="Title", required=True)
    description = fields.Text(string="Description")

    property_type_id = fields.Many2one("estate.property.type", string="Property Type")

    salesperson_id = fields.Many2one(
        "res.users", string="Salesperson", default=lambda self: self.env.user
    )

    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)

    tag_ids = fields.Many2many("estate.property.tag", string="Tags")

    state = fields.Selection(
        [
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
    )

    expected_price = fields.Float(string="Expected Price")

    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False)

    bedrooms = fields.Integer(string="Bedrooms", default=2)

    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer(string="Number of Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area (sqm)")

    garden_orientation = fields.Selection(
        [("north", "North"), ("south", "South"), ("east", "East"), ("west", "West")],
        string="Garden Orientation",
    )

    postcode = fields.Char(string="Postcode")

    date_availability = fields.Date(
        string="Available From",
        copy=False,
        default=lambda self: date.today() + timedelta(days=90),
    )

    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")

    _sql_constraints = [
        (
            "check_expected_price_positive",
            "CHECK(expected_price > 0)",
            "The expected price must be strictly positive.",
        ),
        (
            "check_selling_price_positive",
            "CHECK(selling_price >= 0)",
            "The selling price must be positive or zero.",
        ),
    ]

    total_area = fields.Integer(string="Total Area", compute="_compute_total_area")

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    # Computed Field: Best Offer = max(price from offer_ids)
    best_price = fields.Float(string="Best Offer", compute="_compute_best_price")

    @api.depends("offer_ids.price")  # Dependency path: One2many -> Float
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped("price"))
            else:
                record.best_price = 0.0

    @api.onchange("garden")
    def _onchange_garden(self):
        """Automatically set/reset garden_area and garden_orientation based on garden checkbox."""
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    def action_mark_sold(self):
        for record in self:
            if record.state == "cancelled":
                raise UserError("Cancelled properties cannot be sold.")
            record.state = "sold"
        return True

    def action_cancel_property(self):
        for record in self:
            if record.state == "sold":
                raise UserError("Sold properties cannot be cancelled.")
            record.state = "cancelled"
        return True

    @api.constrains("expected_price", "selling_price")
    def _check_selling_price(self):
        for record in self:
            if float_is_zero(record.selling_price, precision_digits=2):
                continue  # skip if selling_price is 0
            min_acceptable = 0.9 * record.expected_price
            if (
                float_compare(record.selling_price, min_acceptable, precision_digits=2)
                < 0
            ):
                raise ValidationError(
                    "Selling price must be at least 90% of the expected price."
                )

    @api.ondelete(at_uninstall=False)
    def _check_can_be_deleted(self):
        for record in self:
            if record.state not in ["new", "cancelled"]:
                raise UserError(
                    "Only properties in 'New' or 'Cancelled' state can be deleted."
                )
