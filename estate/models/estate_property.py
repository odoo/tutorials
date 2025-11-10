from dateutil.relativedelta import relativedelta
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        "Availability Date",
        default=lambda self: fields.Date.today() + relativedelta(months=3)
    )
    expected_price = fields.Float("Expected Price", required=True)
    selling_price = fields.Float("Selling Price", readonly=True)
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
        ],
        string="Garden Orientation",
    )
    state = fields.Selection(
        [
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        string="Status",
        required=True,
        copy=False,
        default="new",
    )
    active = fields.Boolean(default=True)
    property_type_id = fields.Many2one("estate.property.type", "Property Type")
    buyer_id = fields.Many2one("res.partner", "Buyer", copy=False)
    salesperson_id = fields.Many2one("res.users", string="Salesperson")
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    total_area = fields.Integer("Total Area (sqm)", compute="_compute_total_area")
    best_price = fields.Float("Best Offer", compute="_compute_best_price")

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = (record.living_area or 0) + (record.garden_area or 0)

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped("price") or [0])

    @api.onchange("garden")
    def _onchange_garden(self):
        for record in self:
            if record.garden:
                if record.garden_area == 10:
                    record.garden_orientation = "north"
                elif record.garden_area == 20:
                    record.garden_orientation = "south"
                elif record.garden_area == 30:
                    record.garden_orientation = "east"
                elif record.garden_area == 40:
                    record.garden_orientation = "west"
                else:
                    record.garden_area = 0
                    record.garden_orientation = False
            else:
                record.garden_area = 0
                record.garden_orientation = False

    def action_cancel(self):
        for record in self:
            if record.state == "sold":
                raise UserError("A sold property cannot be cancelled")
            record.state = "cancelled"

    def action_sold(self):
        for record in self:
            if record.state == "cancelled":
                raise UserError("A cancelled property cannot be set as sold")
            record.state = "sold"

    _constraints = [
        models.CheckConstraint(
            "expected_price > 0",
            message="The expected price must be strictly positive.",
        ),
        models.CheckConstraint(
            "selling_price >= 0",
            message="The selling price must be positive.",
        ),
    ]

    @api.constrains("selling_price", "expected_price")
    def _check_selling_price_ratio(self):
        for record in self:
            if not float_is_zero(record.selling_price, precision_digits=2):
                if (
                    float_compare(
                        record.selling_price,
                        record.expected_price * 0.9,
                        precision_digits=2,
                    )
                    < 0
                ):
                    raise ValidationError(
                        "The selling price cannot be lower than 90% of the expected price."
                    )
