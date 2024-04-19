from odoo import api, fields, models

from odoo.exceptions import UserError, ValidationError

from datetime import date
from dateutil.relativedelta import relativedelta

from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate property"
    _order = "id desc"
    _sql_constraints = [
        (
            "check_expected_price",
            "CHECK(expected_price > 0)",
            "The expected price must be stricly positive",
        ),
        (
            "check_selling_price",
            "CHECK(selling_price >= 0)",
            "The selling price must be stricly positive",
        ),
    ]

    name = fields.Char("Title", required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        "Available From", default=(date.today() + relativedelta(months=+3)), copy=False
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer("Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer("Garden Area (sqm)")
    garden_orientation = fields.Selection(
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ]
    )
    active = fields.Boolean("Active", default=True)
    state = fields.Selection(
        required=True,
        copy=False,
        default="new",
        selection=[
            ("new", "New"),
            ("offer received", "Offer Received"),
            ("offer accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("canceled", "Canceled"),
        ],
    )
    property_type_id = fields.Many2one("estate.property.type")
    partner_id = fields.Many2one("res.partner", string="Buyer")
    user_id = fields.Many2one(
        "res.users", string="Salesman", default=lambda self: self.env.user
    )
    tag_ids = fields.Many2many("estate.property.tag")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    total_area = fields.Integer(compute="_compute_total_area")
    best_price = fields.Float(compute="_compute_best_offer", string="Best Offer")

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_offer(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped("price"), default=0)

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = False
            self.garden_orientation = False

    @api.constrains("selling_price", "expected_price")
    def _check_selling_price(self):
        for record in self:
            if (
                float_compare(
                    value1=record.selling_price,
                    value2=(record.expected_price * 0.9),
                    precision_digits=2,
                )
                < 0
            ) and (not float_is_zero(value=record.selling_price, precision_digits=2)):
                raise ValidationError(
                    "The selling price must be at least 90% of the expected price"
                )

    def action_set_property_sold(self):
        for record in self:
            if record.state == "canceled":
                raise UserError("You cannot sell a canceled property")

            record.state = "sold"
        return True

    def action_set_property_canceled(self):
        for record in self:
            if record.state == "sold":
                raise UserError("You cannot cancel a sold property")

            record.state = "canceled"
        return True
