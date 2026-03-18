from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero
from dateutil.relativedelta import relativedelta
import datetime


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    _order = "id desc"

    name = fields.Char(required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char()
    date_availability = fields.Date(
        string="Available From",
        copy=False,
        default=datetime.date.today() + relativedelta(months=3),
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
        [("north", "North"), ("east", "East"), ("south", "South"), ("west", "West")]
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        string="Status",
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
    salesman = fields.Many2one(
        "res.users",
        string="Salesperson",
        index=True,
        default=lambda self: self.env.user,
    )
    buyer = fields.Many2one("res.partner", string="Buyer", copy=False)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    total_area = fields.Integer(compute="_compute_total_area")
    best_price = fields.Float(compute="_compute_best_price", string="Best Price")

    _check_expected_price = models.Constraint(
        "CHECK(expected_price > 0)",
        "Expected price must be greater than 0",
    )
    _check_selling_price = models.Constraint(
        "CHECK(selling_price >= 0)",
        "Selling price must be greater or equal to 0",
    )

    @api.ondelete(at_uninstall=False)
    def unlink_if_property_not_new_or_cancelled(self):
        for record in self:
            if record.state not in ('new', 'cancelled'):
                raise UserError("Properties can only be deleted in 'New' or 'Cancelled' state")

    # -------------------------------------------------------------------------
    # COMPUTE METHODS
    # -------------------------------------------------------------------------

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends()
    def _compute_best_price(self):
        for record in self:
            record.best_price = (
                max(record.offer_ids.mapped("price")) if record.offer_ids else 0
            )

    @api.onchange("garden")
    def _onchange_partner_id(self):
        if self.garden:
            self.garden_area = self.garden_area or 10
            self.garden_orientation = self.garden_orientation or "north"
        else:
            self.garden_area = 0
            self.garden_orientation = None

    def action_sold(self):
        for record in self:
            if record.state == "cancelled":
                raise UserError("Cancelled properties cannot be sold.")
            else:
                record.state = "sold"
        return True

    def action_cancel(self):
        for record in self:
            if record.state == "sold":
                raise UserError("Sold properties cannot be cancelled.")
            else:
                record.state = "cancelled"
        return True

    @api.constrains("selling_price", "expected_price")
    def check_selling_price(self):
        for record in self:
            if not float_is_zero(record.selling_price, precision_digits=2):
                if float_compare(record.selling_price, record.expected_price * 0.9, 2) < 0:
                    raise ValidationError(
                        "The selling price cannot be lower than 90% of the expected price."
                    )
