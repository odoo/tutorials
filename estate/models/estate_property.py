from datetime import timedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class Property(models.Model):
    _name = "estate.property"
    _description = "estate property details"
    _order = "id desc"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        copy=False, default=lambda self: fields.Date.today() + timedelta(days=90)
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living Area(sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string="Garden Area(sqm)", store=True)
    garden_orientation = fields.Selection(
        selection=[
            ("north", "North"),
            ("west", "West"),
            ("east", "East"),
            ("south", "South"),
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
        default="new",
        copy=False,
        required=True,
    )

    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    salesperson_id = fields.Many2one(
        "res.users", string="Salesman", default=lambda self: self.env.user
    )
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False, readonly=True)
    tag_ids = fields.Many2many("estate.property.tag", string="Property Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id")
    total_area = fields.Float(string="Total Area(sqm)", compute="_compute_total_area")
    best_price = fields.Float(
        string="Best Offer", compute="_compute_best_offer", readonly=True, copy=False
    )
    _check_expected_price = models.Constraint(
        "CHECK(expected_price > 0)",
        "The expected price should be strictly positive",
    )
    _check_selling_price = models.Constraint(
        "CHECK(selling_price >= 0)",
        "The selling price should be strictly positive",
    )

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids")
    def _compute_best_offer(self):
        for record in self:
            prices = record.offer_ids.mapped("price")
            if prices:
                record.best_price = max(prices)
            else:
                record.best_price = 0.0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    @api.constrains("selling_price", "expected_price")
    def _check_price(self):
        if not float_is_zero(self.selling_price, precision_rounding=0.001) and (
            float_compare(
                self.selling_price,
                self.expected_price * 0.9,
                precision_rounding=0.01,
            )
            == -1
        ):
            raise ValidationError(
                "The selling price must be at least 90% of the expected price"
            )

    def action_sold_button(self):
        if self.filtered(lambda x: x.state == "cancelled"):
            raise UserError(_("Cancelled Property cannot be sold."))
        else:
            self.state = "sold"
            return {
                "effect": {
                    "fadeout": "no",
                    "message": "helloo",
                    "type": "rainbow_man",
                }
            }

    def action_cancel_button(self):
        if self.filtered(lambda x: x.state == "sold"):
            raise UserError(_("Sold Property cannot be Cancelled."))
        self.state = "cancelled"

    @api.ondelete(at_uninstall=False)
    def _unlink_check_state_before_deletion(self):
        for record in self:
            if record.state not in ["new", "cancelled"]:
                raise UserError(
                    _("You can only delete properties that are 'New' or 'Cancelled'.")
                )
