from odoo.exceptions import UserError, ValidationError
from odoo.tools.date_utils import add
from odoo.tools.float_utils import float_compare, float_is_zero
from odoo import _, api, fields, models


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate property model"
    _order = "id desc"

    active = fields.Boolean("Active", default=True)
    state = fields.Selection([
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        string="Status",
        default="new",
        required=True,
        copy=False,
    )

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=lambda self: add(fields.Date.today(), months=3), string="Available From")
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer()
    has_garage = fields.Boolean()
    has_garden = fields.Boolean()
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
    )
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    buyer = fields.Many2one("res.partner", copy=False)
    salesperson = fields.Many2one("res.users", default=lambda self: self.env.user, string="Salesman")
    tag_ids = fields.Many2many("estate.property.tag")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    total_area = fields.Integer(compute="_compute_total_area", string="Total Area (sqm)")
    best_price = fields.Float(compute="_compute_best_offer", string="Best Offer")

    _expected_price_strictly_positive_constraint = models.Constraint(
        "CHECK(expected_price > 0)",
        "The expected price should be strictly greater than 0!",
    )

    _selling_price_positive_constraint = models.Constraint(
        "CHECK(selling_price >= 0)",
        "The selling price should be greater or equal to 0!",
    )

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_offer(self):
        for record in self:
            if record.offer_ids:
                prices = record.offer_ids.mapped("price")
                record.best_price = max(prices) if prices else 0.0
            else:
                record.best_price = 0.0

    @api.onchange("has_garden")
    def _onchange_has_garden(self):
        if self.has_garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    @api.constrains("selling_price", "expected_price")
    def _check_selling_price(self):
        for record in self:
            if float_is_zero(record.selling_price, precision_digits=2):
                continue

            if float_compare(record.selling_price, 0.9 * record.expected_price, precision_digits=2) < 0:
                raise ValidationError(_("The selling price must be at leat 90% of the expected price ! You must reduce the expected price if you want to accept this order !"))

    @api.ondelete(at_uninstall=False)
    def _unlink_if_new_or_cancelled(self):
        for record in self:
            if record.state not in ("new", "cancelled"):
                raise UserError(_("You can't deleted a property whish isn't new or cancelled !"))

    def mark_order_as_sold(self):
        if "cancelled" in self.mapped("state"):
            raise UserError(_("Cancelled properties cannot be sold"))
        self.state = "sold"
        return True

    def mark_order_as_cancelled(self):
        if "sold" in self.mapped("state"):
            raise UserError(_("Sold properties cannot be cancelled"))
        self.state = "cancelled"
        return True
