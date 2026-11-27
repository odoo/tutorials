from dateutil.relativedelta import relativedelta
from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"
    _order = "id desc"

    def _default_date_availability(self):
        return fields.Date.today() + relativedelta(months=3)

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        copy=False,
        default=_default_date_availability,
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer()
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string="Garden orientation",
        selection=[
            ("north", "North"),
            ("west", "West"),
            ("south", "South"),
            ("east", "East"),
        ],
        help="Orientation of the garden",
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
    property_type_id = fields.Many2one("estate.property.type", string="Type")
    salesperson_id = fields.Many2one(
        "res.users", string="Salesperson", default=lambda self: self.env.user
    )
    # region computed fields
    total_area = fields.Integer(
        compute="_compute_total_area", string="Total Area (sqm)"
    )
    best_price = fields.Float(compute="_compute_best_price", string="Best Price")
    # endregion

    # region relationships
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    # endregion

    # region constraints
    _check_expected_price = models.Constraint(
        "CHECK(expected_price > 0)", "The expected price must be strictly positive."
    )
    _check_selling_price = models.Constraint(
        "CHECK(selling_price >= 0)", "The selling price must be positive."
    )

    @api.constrains("expected_price", "selling_price")
    def _check_price_difference(self):
        for record in self:
            if (
                not float_is_zero(record.selling_price, precision_digits=2)
                and float_compare(
                    record.selling_price,
                    record.expected_price * 0.90,
                    precision_digits=2,
                )
                < 0
            ):
                raise ValidationError(
                    self.env._(
                        "The selling price cannot be lower than 90% of the expected price."
                    )
                )

    # endregion

    # region private methods
    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped("price"), default=0.0)

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    @api.ondelete(at_uninstall=False)
    def _unlink_on_state_new_or_cancelled(self):
        if any(record.state not in ("new", "cancelled") for record in self):
            raise UserError(
                self.env._("Only new and cancelled properties can be deleted.")
            )

    # endregion

    # region public methods
    def action_sold(self):
        for record in self:
            if not record.offer_ids or not any(
                offer.state == "accepted" for offer in record.offer_ids
            ):
                raise UserError(
                    self.env._(
                        "A property must have an accepted offer before it can be sold."
                    )
                )
            if record.state == "cancelled":
                raise UserError(self.env._("Cancelled properties cannot be sold."))
            record.state = "sold"
        return True

    def action_cancel(self):
        for record in self:
            if record.state == "sold":
                raise UserError(self.env._("Sold properties cannot be cancelled."))
            record.state = "cancelled"
        return True

    # endregion
