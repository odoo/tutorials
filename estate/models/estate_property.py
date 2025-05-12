from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _inherit = ["mail.thread"]
    _description = "Real Estate Property"
    _order = "id desc"

    salesperson_id = fields.Many2one(
        "res.users",
        string="Sales Person",
        default=lambda self: self.env.user,
        required=True,
    )
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    property_type_id = fields.Many2one(
        "estate.property.type", string="Property Type", required=True
    )
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")

    name = fields.Char(required=True)
    description = fields.Text()
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
    best_price = fields.Float(
        string="Best Offer", compute="_compute_best_price", store=True
    )

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
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.onchange("garden")
    def _onchange_garden(self):
        for record in self:
            if record.garden:
                record.garden_area = 10
                record.garden_orientation = "north"
            else:
                record.garden_area = 0
                record.garden_orientation = ""

    @api.depends("offer_ids.offer_price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped("offer_price"), default=0.0)

    def action_cancel(self):
        for record in self:
            if record.state == "sold":
                raise UserError("A sold property cannot be cancelled.")
            record.state = "canceled"

    def action_sold(self):
        for record in self:
            if record.state == "canceled":
                raise UserError("A cancelled property cannot be sold.")

            if record.state != "offer_accepted":
                raise UserError(
                    "You cannot mark a property as sold without accepting an offer."
                )

            record.state = "sold"

        return True

    @api.constrains("selling_price", "expected_price")
    def _check_selling_price(self):
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
        for record in self:
            if record.state not in ("new", "canceled"):
                raise UserError(
                    "You can only delete properties in 'New' or 'Cancelled' state."
                )
