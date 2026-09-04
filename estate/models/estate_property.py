from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"

    name = fields.Char(string="Title", required=True)
    description = fields.Text()
    date_availability = fields.Date(
        string="Available From",
        copy=False,
        default=lambda self: fields.Date.add(fields.Date.today(), months=3),
    )
    expected_price = fields.Float(required=True)
    active = fields.Boolean(default=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    postcode = fields.Char()
    garden_orientation = fields.Selection(
        string="Type",
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
    )
    state = fields.Selection(
        [
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        required=True,
        default="new",
        copy=False,
    )
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    salesperson_id = fields.Many2one(
        "res.users", string="Salesman", default=lambda self: self.env.user
    )
    tags_id = fields.Many2many("estate.property.tag", string="Property Tags")
    offer_ids = fields.One2many("estate.property.offer", inverse_name="property_id")
    total_area = fields.Integer(
        compute="_compute_total_area", string="Total Area", store=True
    )
    best_price = fields.Float(compute="_compute_best_price", string="Best Offer")

    _check_expected_price = models.Constraint(
        "CHECK(expected_price >= 0) ", "Expected Price cannot be negative "
    )
    _check_property_values = models.Constraint(
        "CHECK(living_area >=0 AND garden_area >=0 AND bedrooms >=0 AND facades >=0)",
        "Property Description values must be positive",
    )

    @api.constrains("selling_price", "expected_price")
    def _check_selling_price(self):
        for record in self:
            if not float_is_zero(record.selling_price, precision_digits=2) and (
                float_compare(
                    record.selling_price,
                    record.expected_price * 0.9,
                    precision_digits=2,
                )
                < 0
            ):
                raise ValidationError(
                    "The selling price must be at least 90% of the expected price"
                )

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped("price"))
            else:
                record.best_price = 0.0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            if self._origin:
                self.garden_area = self._origin.garden_area
                self.garden_orientation = self._origin.garden_orientation
            else:
                self.garden_area = 10
                self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    @api.onchange("expected_price")
    def _onchange_expected_price(self):
        if (
            self.expected_price
            and self.best_price
            and self.expected_price < self.best_price
        ):
            return {
                "warning": {
                    "title": "Price Warning",
                    "message": (
                        "The expected price is lower than the current best offer"
                    ),
                    "type": "notification",
                }
            }

    def action_cancel_property(self):
        for record in self:
            if record.state == "sold":
                raise UserError("sold properties cannot be cancelled")
            record.state = "cancelled"

    def action_sold_property(self):
        for record in self:
            if record.state == "cancelled":
                raise UserError("cancelled properties cannot be sold")
            if record.selling_price == 0:
                raise UserError(
                    "Set the selling price by accepting an offer before selling the property"
                )
            record.state = "sold"
