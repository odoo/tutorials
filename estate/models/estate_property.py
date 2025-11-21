from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "estate property model"
    _order = "id desc"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        copy=False, default=fields.Date.today() + relativedelta(months=+3)
    )
    expected_price = fields.Float(required=True, default=1)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
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
        required=True,
        copy=False,
        default="new",
    )
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    buyer_id = fields.Many2one("res.partner", copy=False)
    salesperson_id = fields.Many2one("res.users", default=lambda self: self.env.user)
    property_tag_ids = fields.Many2many("estate.property.tag", string="Propert Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    total_area = fields.Float(compute="_compute_total_area")
    best_price = fields.Float(compute="_compute_best_price")
    _check_positive_expected_price = models.Constraint(
        "CHECK(expected_price > 0)",
        "The Expected Price of a Property must be strictly positive",
    )
    _check_positive_selling_price = models.Constraint(
        "CHECK(selling_price > 0)",
        "The Selling Price of a Property must be strictly positive",
    )

    @api.constrains("expected_price", "selling_price")
    def _check_selling_price(self):
        for property in self:
            percentage = property.selling_price / property.expected_price
            if (
                not float_is_zero(property.selling_price, precision_digits=2)
                and float_compare(percentage, 0.9, precision_digits=2) == -1
            ):
                raise UserError(
                    "selling price cannot be lower than 90% of the expected price"
                )

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        self.ensure_one()
        for property in self:
            property.total_area = property.living_area + property.garden_area

    @api.depends("offer_ids")
    def _compute_best_price(self):
        self.ensure_one()
        for property in self:
            property.best_price = max(property.offer_ids.mapped("price") or [0])

    @api.onchange("garden")
    def _onchange_garden(self):
        self.garden_area = 10 if self.garden else 0
        self.garden_orientation = "north" if self.garden else ""

    @api.ondelete(at_uninstall=False)
    def _unlink_if_new_or_cancelled_state(self):
        if any(
            not (property.state == "new" or property.state == "cancelled")
            for property in self
        ):
            raise UserError("You can only delete new or cancelled properties")

    def action_sold(self):
        self.ensure_one()
        for property in self:
            if property.state == "cancelled":
                raise UserError("You cannot sell a cancelled property")
            property.state = "sold"
        return True

    def action_cancel(self):
        self.ensure_one()
        for property in self:
            if property.state == "sold":
                raise UserError("You cannot cancel a sold property")
            property.state = "cancelled"
        return True
