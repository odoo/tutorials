from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "real estate property"
    _order = "id desc"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        string="Date Availability",
        copy=False,
        default=fields.Date.add(fields.Date.today(), months=3),
    )
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living Area", default=0)
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string="Garden Area")
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
        help="Orientation is used to determine garden orientation",
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        string="State",
        selection=[
            ("new", "New"),
            ("offer received", "Offer Received"),
            ("offer accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("canceled", "Canceled"),
        ],
        required=True,
        copy=False,
        default="new",
        help="State is the current offer status of the property",
    )
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    salesman_id = fields.Many2one(
        "res.users", string="Salesman", index=True, default=lambda self: self.env.user
    )
    buyer_id = fields.Many2one("res.partner", string="Buyer", index=True, copy=False)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offer")
    total_area = fields.Integer(string="Total Area", compute="_compute_total_area")
    best_price = fields.Float(string="Best Price", compute="_compute_best_price")

    _sql_constraints = [
        (
            "check_expected_price",
            "CHECK(expected_price > 0)",
            "The expected price must a positive number",
        ),
        (
            "check_selling_price",
            "CHECK(selling_price > 0)",
            "The selling price must be a positive number",
        ),
    ]

    @api.constrains("selling_price", "expected_price")
    def _check_selling_price(self):
        for record in self:
            if float_is_zero(record.selling_price, precision_rounding=2):
                continue

            if (
                float_compare(
                    record.selling_price,
                    record.expected_price * 0.9,
                    precision_rounding=2,
                )
                < 0
            ):
                raise ValidationError(
                    "The selling price cannot bet lower than 90% of the expected price"
                )

    @api.ondelete(at_uninstall=False)
    def _unlink_if_state_new_or_canceled(self):
        if any(record.state not in ("new", "canceled") for record in self):
            raise UserError("Can't delete an activity that is not new or canceled!")
        return super().unlink()

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped("price"), default=0.0)

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10.0
            self.garden_orientation = "north"
        else:
            self.garden_area = self.garden_orientation = None

    def property_sold(self):
        for record in self:
            if record.state == "canceled":
                raise UserError("Property already canceled")
            record.state = "sold"
        return True

    def property_canceled(self):
        for record in self:
            if record.state == "sold":
                raise UserError("Property already sold")
            record.state = "canceled"
        return True
