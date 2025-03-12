from datetime import date, timedelta
from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Model"
    _order = "id desc"

    name = fields.Char(required=True)
    description = fields.Text()
    expected_price = fields.Float(required=True)
    postcode = fields.Char(required=True)
    date_availability = fields.Date(
        default=lambda self: date.today() + timedelta(days=90),
        copy=False,
    )
    selling_price = fields.Float(copy=False, readonly=True)
    bedrooms = fields.Integer(required=True, default=2)
    living_area = fields.Integer(required=True)
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    total_area = fields.Float(compute="_compute_total_area")
    garden_orientation = fields.Selection(
        [("north", "North"), ("south", "South"), ("east", "East"), ("west", "West")],
        string="Garden Orientation",
    )

    active = fields.Boolean(default=True)
    state = fields.Selection(
        [
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        string="Status",
        copy=False,
        default="new",
    )

    property_type_id = fields.Many2one(
        "estate.property.type", string="Property Type", ondelete="cascade"
    )
    buyer = fields.Many2one("res.partner", string="Buyer", ondelete="cascade")
    salesperson = fields.Many2one(
        "res.users",
        string="Sales Person",
        ondelete="cascade",
        default=lambda self: self.env.user,
    )
    tags_ids = fields.Many2many("estate.tags", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string=" ")
    best_price = fields.Float(compute="_compute_best_price")

    _sql_constraints = [
        (
            "positive_expected_price",
            "CHECK(expected_price > 0)",
            "Expected Price should be positive.",
        ),
        (
            "positive_selling_price",
            "CHECK(selling_price >=0 OR state !='sold')",
            "Can't have selling price less than 0.",
        ),
    ]

    @api.constrains("selling_price", "expected_price")
    def _check_price_90_percentage(self):
        for record in self:
            if (
                not float_is_zero(record.selling_price, precision_rounding=0.01)
                and float_compare(
                    record.selling_price,
                    0.9 * record.expected_price,
                    precision_rounding=0.01,
                )
                < 0
            ):
                raise ValidationError(
                    "The offer price can't be less than 90`%` of the expected price."
                )

    @api.ondelete(at_uninstall=False)
    def _check_state(self):
        for record in self:
            if record.state not in ["new", "cancelled"]:
                raise ValidationError(
                    "Can't delete property unless in New or Cancelled state!"
                )

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden == True:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped("price"), default=0)

    def action_set_sold(self):
        if self.state == "cancelled":
            raise UserError("You cannot mark a cancelled property as sold.")
        self.state = "sold"
        self.active = False
        return True

    def action_set_cancel(self):
        if self.state == "sold":
            raise UserError("You cannot mark a sold property as cancelled.")
        self.state = "cancelled"
        self.active = False
        return True
