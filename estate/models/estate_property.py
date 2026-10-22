from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate property"
    _order = "id desc"

    name = fields.Char(required=True, translate=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        copy=False,
        default=lambda self: fields.Datetime.today() + relativedelta(months=3),
    )
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer("Garden area (sqm)")
    garden_orientation = fields.Selection(
        [("north", "North"), ("south", "South"), ("west", "West"), ("east", "East")]
    )
    active = fields.Boolean(default=True)
    status = fields.Selection(
        [
            ("new", "New"),
            ("offer_received", "Offer received"),
            ("offer_accepted", "Offer accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        required=True,
        copy=False,
        default="new",
    )
    property_type_id = fields.Many2one("estate.property.type")
    salesperson_id = fields.Many2one("res.users", default=lambda self: self.env.user)
    buyer_id = fields.Many2one("res.partner", copy=False)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    total_area = fields.Integer(compute="_compute_total_area")
    expected_price = fields.Float()
    selling_price = fields.Float(readonly=True, copy=False)
    best_price = fields.Float(compute="_compute_best_price")

    _check_expected_price = models.Constraint(
        "CHECK(expected_price > 0)",
        "The expected price must be strictly positive.",
    )
    _check_selling_price_positive = models.Constraint(
        "CHECK(selling_price >= 0)",
        "The selling price must be positive.",
    )

    @api.depends("garden_area", "living_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped("price"), default=0)

    @api.constrains("selling_price", "expected_price")
    def _check_selling_price(self):
        for record in self:
            if (
                not float_is_zero(record.selling_price, 2)
                and float_compare(record.selling_price, 0.9 * record.expected_price, 2)
                == -1
            ):
                raise ValidationError(
                    self.env._(
                        "The selling price cannot be lower than 90% of the expected price."
                    )
                )

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = None
            self.garden_orientation = None

    def action_sold(self):
        for record in self:
            if record.status != "cancelled":
                record.status = "sold"
            else:
                raise UserError(self.env._("A cancelled property can't be sold"))
        return True

    def action_cancel(self):
        for record in self:
            if record.status != "sold":
                record.status = "cancelled"
            else:
                raise UserError(self.env._("A sold property can't be cancelled"))
        return True
