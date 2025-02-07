from datetime import timedelta, date
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero
from odoo import models, fields, api


class EstateProperty(models.Model):
    _name = "estate.property"

    _description = "Property"

    _order = "id desc"

    active = fields.Boolean(string="active", default=True)

    state = fields.Selection(
        [
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("cancelled", "Cancelled"),
            ("sold", "Sold"),
        ],
        default="new",
        required=True,
        copy=False,
    )

    name = fields.Char(string="Property Name", required=True)

    property_type_id = fields.Many2one("estate.property.type", string="Property Type")

    sales_man = fields.Many2one(
        "res.partner", string="Salesman", default=lambda self: self.env.user
    )

    buyer_id = fields.Many2one("res.partner", string="Buyer")

    description = fields.Text(string="Description")

    selling_price = fields.Float(readonly=True, copy=False)

    postcode = fields.Char(string="Postcode")

    availability_date = fields.Date(
        string="Availability date",
        default=lambda self: date.today() + timedelta(days=90),
        copy=False,
    )

    expected_price = fields.Float(string="Expected Price", required=True)

    bedrooms = fields.Integer(string="Number of Bedrooms", default=2)

    living_area = fields.Integer(string="Living Area (sqm)")

    facades = fields.Integer(string="Number of Facades")

    garage = fields.Boolean(string="Garage")

    garden = fields.Boolean(string="Garden")

    garden_area = fields.Integer(string="Garden Area (sqm)")

    garden_orientation = fields.Selection(
        [("north", "North"), ("south", "South"), ("east", "East"), ("west", "West")],
        string="Garden Orientation",
    )

    tag_ids = fields.Many2many("estate.property.tag", string="Tags")

    offer_ids = fields.One2many(
        "estate.property.offer", "property_id", string="Property Offers"
    )

    total_area = fields.Float(
        string="Total Area (sqm)", compute="_total_area", copy=True
    )

    _sql_constraints = [
        (
            "check_expected_price",
            "CHECK(expected_price > 0)",
            "The expected price must be strictly positive.",
        ),
        (
            "check_selling_price",
            "CHECK(selling_price >= 0)",
            "The selling price must be positive.",
        ),
    ]

    @api.depends("living_area", "garden_area")
    def _total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    best_price = fields.Float(string="Best Offer", compute="_best_price")

    @api.depends("offer_ids", "offer_ids.price")
    def _best_price(self):
        for property in self:
            property.best_price = max(property.offer_ids.mapped("price"), default=0)

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    def action_cancel(self):
        for record in self:
            if record.state == "sold":
                raise UserError("A sold property cannot be cancelled.")
            record.state = "cancelled"
        return True

    def action_sold(self):
        for record in self:
            if record.state == "cancelled":
                raise UserError("A cancelled property cannot be marked as sold.")
            record.state = "sold"
        return True

    @api.constrains("selling_price", "expected_price")
    def _check_selling_price(self):
        for record in self:
            # If selling_price is zero, skip the validation (no offer has been validated yet)
            if float_is_zero(record.selling_price, precision_rounding=0.01):
                continue

            # selling_price is at least 90% of expected_price
            minimum_price = record.expected_price * 0.9
            if (
                float_compare(
                    record.selling_price, minimum_price, precision_rounding=0.01
                )
                < 0
            ):
                raise ValidationError(
                    (
                        "The selling price cannot be lower than 90% of the expected price. "
                        "Please adjust the selling price or expected price."
                    )
                )

    def update_state_based_on_offers(self):
        for property in self:
            if not property.offer_ids:  # No offers exist
                property.state = "new"
            elif all(
                offer.status == "refused" for offer in property.offer_ids
            ):  # All offers refused
                property.state = "new"
            else:  # At least one non-refused offer
                property.state = "offer_received"


