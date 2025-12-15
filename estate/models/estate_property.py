from dateutil.relativedelta import relativedelta
from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate property"
    _order = "id desc"

    name = fields.Char(string="Title", required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(string="Available From", default=lambda self: fields.Date.context_today(self) + relativedelta(months=3), copy=False)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        selection=[("north", "North"), ("south", "South"), ("east", "East"), ("west", "West")],
    )

    # Reserved fields
    active = fields.Boolean(default=True)
    state = fields.Selection(
        required=True,
        selection=[("new", "New"), ("offer_received", "Offer Received"), ("offer_accepted", "Offer Accepted"), ("sold", "Sold"), ("cancelled", "Cancelled")],
        default="new",
        copy=False,
        string="Status",
    )

    # Relations
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    salesman_id = fields.Many2one("res.users", default=lambda self: self.env.user)
    buyer_id = fields.Many2one("res.partner", copy=False)
    tag_ids = fields.Many2many("estate.property.tag")
    offer_ids = fields.One2many("estate.property.offer", "property_id")

    # Computed
    total_area = fields.Integer(compute="_compute_total_area", string="Total Area (sqm)")
    best_price = fields.Float(compute="_compute_best_price", string="Best Offer")

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self) -> None:
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self) -> None:
        for record in self:
            record.best_price = max(record.offer_ids.mapped("price"), default=0)

    # Methods that trigger on changes
    @api.onchange("garden")
    def _onchange_garden_defaults(self) -> None:
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = None
            self.garden_orientation = None

    @api.ondelete(at_uninstall=False)
    def _unlink_except_new_or_cancelled(self) -> None:
        if any(record.state not in {"new", "cancelled"} for record in self):
            raise UserError(self.env._("Cannot delete properties unless they are new or cancelled."))

    # Public methods
    def action_set_sold(self) -> bool:
        for record in self:
            if record.state == "sold":
                continue

            if record.state == "cancelled":
                raise UserError(record.env._("Cancelled properties cannot be sold."))

            record.state = "sold"
        return True

    def action_set_cancelled(self) -> bool:
        for record in self:
            if record.state == "cancelled":
                continue

            if record.state == "sold":
                raise UserError(record.env._("Sold properties cannot be cancelled."))

            record.state = "cancelled"
        return True

    # Constraints
    _check_expected_price_strict_positive = models.Constraint(
        "CHECK(expected_price > 0)",
        "A property's expected price must be strictly greater than 0.",
    )

    _check_selling_price_positive = models.Constraint(
        "CHECK(selling_price >= 0)",
        "A property's selling price must be equal to or greater than 0.",
    )

    @api.constrains("expected_price", "selling_price")
    def _check_selling_price_percentage(self) -> None:
        for record in self:
            # Selling price is zero when no offer has been accepted
            if not float_is_zero(record.selling_price, precision_digits=2) and float_compare(record.selling_price, 0.9 * record.expected_price, precision_digits=2) < 0:
                raise ValidationError(record.env._("A property's selling price cannot be lower than 90 percent of its expected price."))
