from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    _order = "id desc"

    active = fields.Boolean(default=True)
    state = fields.Selection(
        string="State",
        copy=False,
        default="new",
        required=True,
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
    )
    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        default=(fields.Date.today() + relativedelta(months=3)),
        copy=False,
    )
    seller_id = fields.Many2one(
        "res.users",
        string="Sales Person",
        default=lambda self: self.env.user,
    )
    buyer_id = fields.Many2one("res.partner", string="Buyer")

    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    best_price = fields.Float(compute="_compute_best_price")
    property_tag_ids = fields.Many2many("estate.property.tag", string="Property Tags")
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer("Property Garden Area")
    total_area = fields.Integer(compute="_compute_total_area")
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
        help="Select garden orientation",
    )

    _check_expected_price = models.Constraint(
        "CHECK(expected_price > 0)",
        "Expected price should be positive.",
    )
    _check_selling_price = models.Constraint(
        "CHECK(selling_price > 0)",
        "Selling price must be positive.",
    )

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for property in self:
            property.total_area = property.living_area + property.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for property in self:
            property.best_price = max(property.offer_ids.mapped("price"), default=0)

    @api.onchange("garden")
    def _onchange_garden(self):
        for property in self:
            if property.garden:
                property.garden_area = 10
                property.garden_orientation = "north"
            else:
                property.garden_area = None
                property.garden_orientation = None

    def action_cancel_property(self):
        for property in self:
            if property.state == "sold":
                raise UserError(_("Sold properties cannot be cancelled."))
        property.state = "cancelled"
        return True

    def action_sold_property(self):
        for property in self:
            if property.state == "cancelled":
                raise UserError(_("Cancelled properties cannot be sold."))
        property.state = "sold"
        return True

    @api.constrains("selling_price")
    def _check_selling_price(self):
        for property in self:
            selling_price = property.selling_price
            expected_price = property.expected_price
            if (
                not float_is_zero(property.selling_price, precision_digits=2)
                and float_compare(
                    selling_price,
                    0.9 * expected_price,
                    precision_digits=2,
                )
                == -1
            ):
                raise ValidationError(
                    _("Selling price is not atleast 90% of expected price."),
                )

    @api.ondelete(at_uninstall=False)
    def _ensure_state_before_deletion(self):
        for property in self:
            if property.state in ("new", "cancelled"):
                raise UserError(_("can't delete a properties in intermediate states."))
