from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero

from odoo import api, fields, models


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    _order = "id desc"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        copy=False, default=lambda self: fields.Date.add(fields.Date.today(), months=3)
    )
    expected_price = fields.Integer(required=True)
    selling_price = fields.Integer(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(default=0)
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(default=0)
    garden_orientation = fields.Selection(
        string="orientation",
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        string="State",
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        required=True,
        default="new",
    )
    estate_property_type_id = fields.Many2one(
        "estate.property.type", string="Property Type"
    )
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False, readonly=True)
    salesperson_id = fields.Many2one(
        "res.users", string="Salesman", default=lambda self: self.env.user
    )
    estate_property_tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    estate_property_offer_ids = fields.One2many("estate.property.offer", "property_id")
    total_area = fields.Integer(compute="_compute_total_area")
    best_price = fields.Float(compute="_compute_best_price")

    _check_expected_price_positive = models.Constraint(
        "CHECK(expected_price > 0)",
        "A property expected price must be strictly positive.",
    )
    _check_selling_price_positive = models.Constraint(
        "CHECK(selling_price > 0)", "A property selling price must be positive"
    )

    @api.depends("living_area", "garden_area", "garden")
    def _compute_total_area(self):
        for property in self:
            property.total_area = (
                property.living_area + property.garden_area
                if property.garden
                else property.living_area
            )

    @api.depends("estate_property_offer_ids.price")
    def _compute_best_price(self):
        for property in self:
            property.best_price = (
                max(property.estate_property_offer_ids.mapped("price"))
                if property.estate_property_offer_ids
                else None
            )

    @api.onchange("garden")
    def _onchange_has_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"

    def action_sell(self):
        for property in self:
            if property.state == "cancelled":
                raise UserError("You can't sell a a cancelled property :)")

            property.state = "sold"
            return True

    def action_cancel(self):
        for property in self:
            if property.state == "sold":
                raise UserError("you can't cancel a sold property :)")

            property.state = "cancelled"
            return True

    @api.constrains("selling_price", "expected_price")
    def _check_expected_to_selling(self):
        for property in self:
            if (
                not float_is_zero(property.selling_price, precision_digits=2)
            ) and float_compare(
                property.selling_price,
                property.expected_price * 0.9,
                precision_digits=2,
            ) == -1:
                raise ValidationError(
                    r"the selling price cannot be lower than 90% of the expected price"
                )
