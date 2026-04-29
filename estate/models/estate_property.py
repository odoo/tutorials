from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class Property(models.Model):
    # Model definition
    _name = "estate.property"
    _description = "Estate Property"
    _order = "id desc"
    _check_expected_price = models.Constraint(
        "CHECK(expected_price > 0)",
        "The expected price should be strictly positive.",
    )

    # Fields
    name = fields.Char("Title", required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        "Available From",
        default=datetime.today() + relativedelta(months=3),
        copy=False,
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(
        readonly=True,
        copy=False,
    )
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer("Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer("Garden Area (sqm)")
    garden_orientation = fields.Selection(
        string="Orientation",
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
    )
    total_area = fields.Integer("Total Area (sqm)", compute="_compute_total_area")
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    buyer_id = fields.Many2one("res.partner", copy=False)
    salesman_id = fields.Many2one("res.users", default=lambda self: self.env.user)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id")
    best_price = fields.Float(compute="_compute_best_price")
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
        store=True,
        compute="_compute_state",
    )

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped("price")) if record.offer_ids else 0.0

    @api.depends("offer_ids")
    def _compute_state(self):
        for record in self:
            if (record.state == "new" and len(record.offer_ids) > 0):
                record.state = "offer_received"

    @api.constrains("expected_price", "selling_price")
    def _check_selling_price_to_expected_price_ratio(self):
        for record in self:
            if (not float_is_zero(record.selling_price, precision_digits=0) and
            float_compare(record.selling_price, record.expected_price * 0.9, precision_digits=0) == -1):
                raise ValidationError("The selling price should be at least 90% of the expected price.")

    @api.onchange("garden")
    def _onchange_garden_values(self):
        self.garden_area = 10 if self.garden else 0
        self.garden_orientation = "north" if self.garden else None

    @api.ondelete(at_uninstall=False)
    def _unlink(self):
        for record in self:
            if record.state in ("new", "cancelled"):
                raise UserError("New or cancelled properties cannot be deleted.")
        return super().unlink()

    def action_cancel_property(self):
        if self.state == "sold":
            raise UserError("Sold properties cannot be cancelled.")
        return self.write({
            "state": "cancelled",
        })

    def action_sold_property(self):
        if self.state == "cancelled":
            raise UserError("Cancelled properties cannot be sold.")
        return self.write({
            "state": "sold",
        })
