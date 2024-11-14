from odoo import models, fields, api
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"

    name = fields.Char(required=True, string="Name")
    postcode = fields.Char(string="pincode")
    date_availability = fields.Date(
        string="Available from",
        default=lambda self: (datetime.now() + relativedelta(months=3)).date(),
        copy=False,
    )
    expected_price = fields.Float(required=True, string="Expected Price")
    selling_price = fields.Float(readonly=True, copy=False)

    description = fields.Char()
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="living area(sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    active = fields.Boolean(default=True)
    garden_area = fields.Integer(string="garden area(sqm)")
    garden_orientation = fields.Selection(
        [
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
    )
    total_area = fields.Float(compute="_compute_total_area", string="total area(sqm)")
    propery_type_id = fields.Many2one("estate.property.types", required=True)
    user_id = fields.Many2one(
        "res.users",
        string="Salesperson",
        index=True,
        default=lambda self: self.env.user,
    )
    partner_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    tag_ids = fields.Many2many("estate.property.tags", string="Tags")
    offer_ids = fields.One2many(
        "estate.property.offers", "property_id", string="Offers"
    )
    best_price = fields.Float(compute="_compute_best_price")

    @api.depends("total_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("state")
    def _update_state_on_offer_received(self):
        for record in self:
            if len(record.offer_ids) > 1:
                record.state = "offer_received"
            else:
                record.state = "new"

    @api.depends("best_price")
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped("price"))
            else:
                record.best_price = 0.0

    @api.onchange("garden")
    def _onchange_garden(self):
        for record in self:
            record.garden_area = 10 if record.garden else 0
            record.garden_orientation = "north" if record.garden else None

    def onclick_sold(self):
        for record in self:
            if record.state not in ["cancelled"]:
                record.state = "sold"
            else:
                raise UserError("cancelled can not be sell")

    def onclick_cancel(self):
        for record in self:
            if record.state not in ["sold"]:
                record.state = "cancelled"
            else:
                raise UserError("sold can not be cancel")

    _sql_constraints = [
        (
            "check_expected_price_cust",
            "CHECK(expected_price > 0)",
            "expected price cannot be less than 0",
        ),
    ]

    @api.constrains("selling_price")
    def _check_selling_price(self):
        for record in self:
            if (
                float_compare(
                    record.selling_price,
                    record.expected_price * 90 / 100,
                    precision_digits=2,
                )
                == -1
            ):
                raise ValidationError(
                    "Selling price is too low! It must be at least 90% of the expected price."
                )
