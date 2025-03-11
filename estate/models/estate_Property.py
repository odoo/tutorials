from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateModel(models.Model):
    _name = "estate.property"
    _description = "Estate model help save data"
    _order = "id desc"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        "Availability From",
        default=lambda self: fields.Date.add(fields.Date.today(), days=90),
        copy=False,
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float("Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer("Number of Bedrooms", default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        [("north", "North"), ("east", "East"), ("south", "South"), ("west", "West")],
        string="Garden Orientation",
    )
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    active = fields.Boolean("Active", default=True)
    state = fields.Selection(
        string="State",
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        default="new",
        copy=False,
        required=True,
    )

    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    salesperson_id = fields.Many2one(
        "res.users",
        string="SalesPerson",
        index=True,  # for index in database
        tracking=True,  # changes to this field -> to be logged in chatter
        default=lambda self: self.env.user,
    )

    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id")

    total_area = fields.Float(compute="_compute_total_area", string="Total Area(sqm)")
    best_price = fields.Float(
        compute="_compute_best_price", string="Best Price", store=True
    )

    _sql_constraints = [
        (
            "check_expected_price",
            "CHECK(expected_price > 0)",
            "Expected price must be strictly positive.",
        ),
        (
            "check_selling_price",
            "CHECK(selling_price >= 0 or state!='sold')",
            "Selling Price must be Positive",
        ),
    ]

    @api.depends("living_area", "garden_area", "garden")
    def _compute_total_area(self):
        for record in self:  # loop in compute and list view multiedit
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped("price"), default=0.0)

    @api.onchange("garden")  # onChange work on ui(form) not in code
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = ""

    def action_cancel_property(self):
        if self.state == "sold":
            raise UserError("Sold Property cannot be cancelled.")
        self.state = "cancelled"

    def action_set_sold_property(self):
        if self.state == "cancelled":
            raise UserError("Cancelled Property cannot be Sold")
        self.state = "sold"

    @api.constrains("expected_price", "selling_price")
    def _check_selling_price(self):
        for record in self:
            if float_is_zero(record.selling_price, precision_digits=2):
                continue

            min_allowed_price = 0.9 * record.expected_price
            if (
                float_compare(
                    record.selling_price, min_allowed_price, precision_digits=2
                )
                == -1
            ):
                raise ValidationError(
                    "Selling Price cannot be lower than 90% of expected price"
                )

    @api.ondelete(at_uninstall=False)
    def _unlink_if_not_new_or_cancelled(self):
        for record in self:
            if record.state not in ["new", "cancelled"]:
                raise UserError(f"Cannot delete property in state {record.state}.")
