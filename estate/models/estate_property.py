from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "real state property"
    _order = "id desc"

    property_type_id = fields.Many2one(
        "estate.property.type",
        string="Property Type",
    )
    buyer_id = fields.Many2one(
        "res.partner",
        string="buyer",
        copy=False,
    )
    salesperson_id = fields.Many2one(
        "res.users",
        string="sales person",
        default=lambda self: self.env.user,
    )
    tag_ids = fields.Many2many(
        "estate.property.tag",
        string="Tags",
    )
    offer_ids = fields.One2many(
        "estate.property.offer",
        "property_id",
        string="Offer",
    )
    maintenance_ids = fields.One2many(
        "maintenance.property",
        "prop_id",
        string="Maintenance"
    )
    name = fields.Char(required=True)
    active = fields.Boolean(default=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        copy=False,
        default=fields.Date.today() + relativedelta(months=3),
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)

    _check_expected_price = models.Constraint(
        "CHECK(expected_price > 0)",
        "Expected price must be strictly positive.",
    )

    _check_selling_price = models.Constraint(
        "CHECK(selling_price IS NULL OR selling_price > 0)",
        "Selling price must be strictly positive when set.",
    )

    @api.constrains("selling_price", "expected_price")
    def _check_selling_price_90_percent(self):
        for property in self:
            if float_is_zero(property.selling_price, precision_rounding=0.01):
                continue
            minimum_price = property.expected_price * 0.90
            if float_compare(
                property.selling_price,
                minimum_price,
                precision_rounding=0.01,
            ) < 0:
                error_msg = "Selling price cannot be lower than 90% of the expected price."
                raise ValidationError(error_msg)

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
        group_expand="_read_group_stage_ids",
        copy=False,
    )

    @api.model
    def _read_group_stage_ids(self, *args, **kwargs):
        return ["new", "offer_received", "offer_accepted", "sold", "cancelled"]

    best_price = fields.Float(compute="_compute_price")
    total_area = fields.Float(compute="_compute_total")

    @api.depends("living_area", "garden_area")
    def _compute_total(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_price(self):
        for property in self:
            if property.offer_ids:
                property.best_price = max(property.offer_ids.mapped("price"))
            else:
                property.best_price = 0.0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    def action_cancel(self):
        for property in self:
            if property.state == "sold":
                message = "A sold property cannot be cancelled."
                raise UserError(message)
            property.state = "cancelled"
        return True

    def action_sold(self):
        for property in self:
            if property.state == "cancelled":
                message = "A cancelled property cannot be set as sold."
                raise UserError(message)
            property.state = "sold"
        return True
