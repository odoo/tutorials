import logging

from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare, float_is_zero

logger = logging.getLogger(__name__)


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real state property"
    _order = "id DESC"

    name = fields.Char(required=True, string="Title")
    description = fields.Text()
    property_type_id = fields.Many2one(
        comodel_name="estate.property.type",
        string="Type",
    )
    postcode = fields.Char()
    date_availability = fields.Date(
        copy=False,
        default=fields.Date.today() + relativedelta(months=3),
        string="Available From",
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
    )
    total_area = fields.Integer(
        compute="_compute_total_area", string="Total Area (sqm)",
    )
    state = fields.Selection(
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        default="new",
    )
    active = fields.Boolean(default=True)
    seller = fields.Many2one(
        comodel_name="res.users",
        string="Salesman",
        default=(lambda self: self.env.user),
    )
    buyer = fields.Many2one(
        comodel_name="res.partner",
        copy=False,
    )
    tag_ids = fields.Many2many(
        comodel_name="estate.property.tag",
        string="Tags",
    )
    offer_ids = fields.One2many(
        comodel_name="estate.property.offer",
        inverse_name="property_id",
        string="Offers",
    )
    best_offer = fields.Float(compute="_compute_best_offer")

    _check_positive_expected_price = models.Constraint(
        "CHECK(expected_price > 0)",
        "Expected Price must be positive!",
    )
    _check_positive_selling_price = models.Constraint(
        "CHECK(selling_price > 0)",
        "Selling Price must be positive!",
    )
    _name_uniq = models.Constraint(
        "UNIQUE(name)",
        "A property with this name already exists!",
    )

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids")
    def _compute_best_offer(self):
        for record in self:
            record.best_offer = (
                max(record.offer_ids.mapped("price")) if record.offer_ids else 0
            )

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = None

    def action_cancel(self):
        for record in self:
            if record.state == 'sold':
                raise UserError("Sold properties cannot be cancelled.")
            record.state = "cancelled"

    def action_sold(self):
        for record in self:
            if record.state == "cancelled":
                raise UserError("Cancelled properties cannot be sold")
            record.state = "sold"

    @api.constrains("selling_price", "expected_price")
    def _check_reasonable_selling_price(self):
        for record in self:
            if (
                not float_is_zero(record.selling_price, precision_digits=2)
                and float_compare(record.selling_price, 0.9 * record.expected_price, precision_digits=2) == -1
            ):
                raise ValidationError("Selling price cannot be lower than 90% of the expected price")
