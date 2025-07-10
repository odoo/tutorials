from dateutil.relativedelta import relativedelta
from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class RecurringPlan(models.Model):
    _name = "estate.property"
    _description = "estate property revenue plans"
    _order = "id desc"  # For ordering in ascending opr descending order   one more way to do so is from view like: <list default_order="date desc">

    name = fields.Char(required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(
        string="Available From",
        copy=False,
        default=lambda self: fields.Date.today() + relativedelta(months=3),
    )
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer(string="Number of Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
        string="Garden Orientation",
        help="Orientation of the garden relative to the property",
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        selection=[
            ("new", "NEW"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        string="Status",
        required=True,
        default="new",
        copy=False,
        # readonly=True
    )

    total_area = fields.Integer(string="Total Area", compute="_compute_total_area")
    best_price = fields.Float(string="Best Offer", compute="_compute_best_price")

    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    user_id = fields.Many2one(
        "res.users", string="Salesman", copy=False, default=lambda self: self.env.user
    )

    tag_id = fields.Many2many("estate.property.tag", string="Tags", copy=False)

    offer_id = fields.One2many("estate.property.offer", "property_id", string="Offer")

    _sql_constraints = [
        (
            "check_expected_price",
            "CHECK(expected_price > 0)",
            "The Expected price of a property should be strictly positive.",
        ),
        (
            "check_selling_price",
            "CHECK(selling_price IS NULL OR selling_price >= 0)",
            "Selling price must be positive when set.",
        ),
    ]

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for area in self:
            area.total_area = area.living_area + area.garden_area

    @api.depends("offer_id.price")
    def _compute_best_price(self):
        for record in self:
            # Get all prices from offer_ids
            offer_prices = record.offer_id.mapped("price")
            record.best_price = max(offer_prices) if offer_prices else 0.0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_orientation = "north"
            self.garden_area = 10
        else:
            self.garden_orientation = False
            self.garden_area = 0

    def action_property_sold(self):
        for prop in self:
            if prop.state == "cancelled":
                raise UserError(_("Cancelled properties cannot be sold."))
            prop.state = "sold"
        return True

    def action_property_cancel(self):
        for prop in self:
            if prop.state == "sold":
                raise UserError(_("Sold properties cannot be cancelled."))
            prop.state = "cancelled"
        return True

    @api.constrains("selling_price", "expected_price")
    def _check_selling_price(self):
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
                    "Selling price cannot be lower than 90% of the expected price. "
                    f"(Minimum allowed: {min_allowed_price:.2f})"
                )

    @api.ondelete(at_uninstall=False)
    def _unlink_except_state_not_new(self):
        for rec in self:
            if rec.state not in ["new", "cancelled"]:
                raise UserError(
                    _(
                        "You cannot delete a property unless its state is 'New' or 'Cancelled'."
                    )
                )
