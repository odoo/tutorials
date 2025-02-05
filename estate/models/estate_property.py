from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_is_zero
from odoo.exceptions import ValidationError


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "This is the estate property model"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        copy=False, default=fields.Date.add(fields.Date.today(), months=3)
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ]
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        selection=[
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
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    salesman_id = fields.Many2one(
        "res.users", string="Salesman", default=lambda self: self.env.user
    )
    buyer_id = fields.Many2one("res.partner", string="Buyer")
    tag_ids = fields.Many2many("estate.property.tag", string="Property Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id")
    total_area = fields.Float(compute="_compute_total_area")
    best_price = fields.Float(compute="_compute_best_offer")

    _sql_constraints = [
        (
            "expected_price_positive",
            "check(expected_price > 0)",
            "Expected Price should be strictly positive.",
        ),
        (
            "selling_price_positive",
            "check(selling_price > 0)",
            "Selling price should strictly be positive",
        ),
    ]

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        print(self)
        for record in self:
            print(record)
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_offer(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped("price"), default=0.0)

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = ""

    def set_as_sold(self):
        for record in self:
            if record.state == "cancelled":
                raise UserError("Cancelled properties cannot be sold.")
            record.state = "sold"
        return True

    def set_as_cancelled(self):
        for record in self:
            if record.state == "sold":
                raise UserError("Sold properties cannot be cancelled.")
            record.state = "cancelled"
        return True

    @api.constrains("selling_price")
    def _selling_price_constraint(self):
        for record in self:
            if record.selling_price < 0.9 * record.expected_price:
                raise ValidationError(
                    "Selling price cannot be lower than 90% of expected price"
                )
