from datetime import timedelta

from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    _order = "name asc"

    name = fields.Char(required=True)
    total_area = fields.Integer(compute="_compute_total_area")

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    def action_sold(self):
        for record in self:
            if record.state == "cancelled":
                raise UserError("Cancelled property cannot be sold.")

            record.state = "sold"

        return True

    def action_cancel(self):
        for record in self:
            if record.state == "sold":
                raise UserError("Sold property cannot be cancelled.")

            record.state = "cancelled"

        return True

    best_price = fields.Float(
        string="Best Offer",
        compute="_compute_best_price",
        store=True,
    )

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for property in self:
            if property.offer_ids:
                property.best_price = max(property.offer_ids.mapped("price"))
            else:
                property.best_price = 0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    property_type_id = fields.Many2one(
        "estate.property.type",
        string="Property Type",
    )

    buyer_id = fields.Many2one(
        "res.partner",
        string="Buyer",
        copy=False,
    )
    salesperson_id = fields.Many2one(
        "res.users",
        string="Salesperson",
        default=lambda self: self.env.user,
    )
    tag_ids = fields.Many2many(
        "estate.property.tag",
        string="Tags",
    )
    offer_ids = fields.One2many(
        "estate.property.offer",
        "property_id",
        string="Offers",
    )

    description = fields.Text()

    postcode = fields.Char()

    date_availability = fields.Date(
        copy=False,
        default=lambda self: fields.Date.today() + timedelta(days=90),
    )

    expected_price = fields.Float()

    selling_price = fields.Float(
        readonly=True,
        copy=False,
    )

    bedrooms = fields.Integer(default=2)

    living_area = fields.Integer()

    facades = fields.Integer()

    garage = fields.Boolean()

    garden = fields.Boolean()

    garden_area = fields.Integer()

    garden_orientation = fields.Selection(
        [
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ]
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
        required=True,
        copy=False,
        default="new",
    )
    _check_selling_price = models.Constraint(
        "CHECK(selling_price >= 0)",
        "A property selling price must be positive",
    )
    _check_expected_price = models.Constraint(
        "CHECK(expected_price > 0)",
        "A property expected price must be strictly positive",
    )

    @api.constrains("selling_price", "expected_price")
    def check_price(self):
        for record in self:
            if float_is_zero(record.selling_price, precision_rounding=0.01):
                continue
            minimum_price = record.expected_price * 0.9

            if (
                float_compare(
                    record.selling_price,
                    minimum_price,
                    precision_rounding=0.01,
                )
                < 0
            ):
                raise ValidationError(
                    " the selling price cannot be lower than 90% of the expected price"
                )
