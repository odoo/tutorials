from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    """Model representing a real estate property in the system.

    This model manages property details, offers, and state transitions for real estate
    transactions. It includes fields for property details, relationships with
    buyers, salespeople, and offers, and computed fields for total area and best offer.
    """

    _name = "estate.property"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Real Estate Property"
    _order = "id desc"

    salesperson_id = fields.Many2one(
        "res.users",
        string="Sales Person",
        default=lambda self: self.env.user,
        required=True,
    )
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    company_id = fields.Many2one(
        "res.company", required=True, default=lambda self: self.env.company
    )
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")

    name = fields.Char(required=True)
    description = fields.Text()
    image = fields.Image(string="Property Image", max_width=2048, max_height=2048)
    postcode = fields.Char()
    date_availability = fields.Date(
        string="Available From", copy=False, default=lambda self: fields.Date.today()
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    garage = fields.Boolean()
    garden = fields.Boolean()
    living_area = fields.Float(string="Living Area (sqm)")
    garden_area = fields.Float(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        [("north", "North"), ("south", "South"), ("east", "East"), ("west", "West")],
        string="Garden Orientation",
    )
    state = fields.Selection(
        [
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("canceled", "Canceled"),
        ],
        string="Status",
        required=True,
        copy=False,
        default="new",
    )
    total_area = fields.Float(
        string="Total Area (sqm)",
        compute="_compute_total_area",
        readonly=True,
        help="Sum of living area and garden area",
    )
    best_price = fields.Float(string="Best Offer", compute="_compute_best_price")

    _sql_constraints = [
        (
            "check_expected_price_positive",
            "CHECK(expected_price >= 0)",
            "The expected price must be strictly positive.",
        ),
        (
            "check_selling_price_positive",
            "CHECK(selling_price >= 0)",
            "The selling price must be strictly positive.",
        ),
        (
            "check_bedrooms_positive",
            "CHECK(bedrooms >= 0)",
            "The number of bedrooms must be zero or positive.",
        ),
    ]

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        """Compute the total area by summing living and garden areas.

        This method updates the `total_area` field for each property record.
        """
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.onchange("garden")
    def _onchange_garden(self):
        """Update garden-related fields when the garden checkbox is toggled.

        If the garden is enabled, sets default garden area to 10 sqm and orientation
        to North. If disabled, clears garden area and orientation.
        """
        for record in self:
            if record.garden:
                record.garden_area = 10
                record.garden_orientation = "north"
            else:
                record.garden_area = 0
                record.garden_orientation = False

    @api.depends("offer_ids.offer_price")
    def _compute_best_price(self):
        """Compute the highest offer price for the property.

        Updates the `best_price` field with the maximum offer price from `offer_ids`.
        If no offers exist, sets `best_price` to 0.0.
        """
        for record in self:
            record.best_price = max(record.offer_ids.mapped("offer_price"), default=0.0)

    def action_cancel(self):
        """Cancel the property listing.

        Changes the property state to 'canceled' unless it is already sold.
        """
        if self.state == "sold":
            raise UserError("A sold property cannot be cancelled.")
        self.state = "canceled"

    def action_sold(self):
        """Mark the property as sold.

        Changes the property state to 'sold' if an offer has been accepted.
        Prevents selling if the property is canceled or no offer is accepted.
        """
        if self.state == "canceled":
            raise UserError("A cancelled property cannot be sold.")

        if self.state != "offer_accepted":
            raise UserError(
                "You cannot mark a property as sold without accepting an offer."
            )
        self.state = "sold"

        return True

    @api.constrains("selling_price", "expected_price")
    def _check_selling_price(self):
        """Validate that the selling price is at least 90% of the expected price.

        This constraint ensures the selling price is not too low compared to the
        expected price, unless the selling price is zero.
        """
        for record in self:
            if float_is_zero(record.selling_price, precision_digits=2):
                continue
            min_acceptable_price = 0.9 * record.expected_price
            if (
                float_compare(
                    record.selling_price, min_acceptable_price, precision_digits=2
                )
                < 0
            ):
                raise ValidationError(
                    "The selling price cannot be lower than 90% of the expected price."
                )

    @api.ondelete(at_uninstall=False)
    def _check_state_before_delete(self):
        """Prevent deletion of properties not in 'new' or 'canceled' states.

        Ensures that properties in active states (e.g., offer received, accepted, or sold)
        cannot be deleted.
        """
        for record in self:
            if record.state not in ("new", "canceled"):
                raise UserError(
                    "You can only delete properties in 'New' or 'Cancelled' state."
                )
