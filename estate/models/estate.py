# Part of Odoo. See LICENSE file for full copyright and licensing details.

from dateutil.relativedelta import relativedelta
from odoo import api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools.float_utils import float_compare
from odoo.tools.translate import _


class Estate(models.Model):
    _name = "estate.property"
    _description = "RE Initial Model"

    name = fields.Char(required=True)
    active = fields.Boolean(default=True)
    description = fields.Char()
    postcode = fields.Char()
    date_availability = fields.Date(
        copy=False, default=lambda self: fields.Date.today() + relativedelta(months=+3)
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
        string="Garden Orientation",
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
    )

    state = fields.Selection(
        string="State",
        required=True,
        readonly=True,
        default="new",
        copy=False,
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Canceled"),
        ],
    )
    property_type_id = fields.Many2one("property.type")
    buyer = fields.Many2one("res.partner", copy=False)
    salesperson = fields.Many2one("res.users", default=lambda self: self.env.user)
    property_tag_ids = fields.Many2many("property.tag")
    property_offer_ids = fields.One2many("property.offer", "property_id")
    total_area = fields.Float(compute="_compute_total_area")
    best_price = fields.Float(compute="_compute_best_price")
    _order = "id desc"

    _sql_constraints = [
        (
            "check_expected_price",
            "CHECK(expected_price > 0)",
            "Expected price must be positive.",
        ),
        (
            "check_selling_price",
            "CHECK(selling_price >= 0)",
            "Selling price must be positive.",
        ),
    ]

    @api.depends("garden_area", "living_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends("property_offer_ids")
    def _compute_best_price(self):
        for record in self:
            if not record.property_offer_ids:
                record.best_price = 0
                continue
            record.best_price = max(record.mapped("property_offer_ids.price"))

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    def action_sell_property(self):
        for record in self:
            record.state = "sold"

    def action_cancel_property(self):
        for record in self:
            record.state = "cancelled"

    @api.constrains("selling_price")
    def _check_selling_price(self):
        for record in self:
            if not record.selling_price:
                continue

            if (
                float_compare(
                    record.selling_price,
                    0.9 * record.expected_price,
                    precision_digits=2,
                )
                < 0
            ):
                raise ValidationError(
                    _(
                        "The selling price cannot be less than 90 percent of the expected price"
                    )
                )

    @api.ondelete(at_uninstall=False)
    def _unlink_if_property_inactive(self):
        for record in self:
            if record.state not in ["new", "cancelled"]:
                raise ValidationError("Can't delete an active property!")
