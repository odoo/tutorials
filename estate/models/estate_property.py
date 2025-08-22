from datetime import date

from odoo import fields, models, api, _
from odoo.tools import date_utils, float_utils
from odoo.exceptions import UserError, ValidationError


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "A property module that adds the property as a listing"
    _sql_constraints = [
        (
            "check_expected_price",
            "CHECK(expected_price > 0)",
            "Expected price of a property should be only positive",
        ),
        (
            "check_selling_price",
            "CHECK(selling_price >= 0)",
            "Selling price of a property should be positive",
        ),
    ]
    _order = "id desc"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        copy=False, default=lambda _: date_utils.add(date.today(), months=3)
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string="Orientation",
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
    )
    total_area = fields.Float(compute="_compute_total_area")
    active = fields.Boolean(default=True)
    state = fields.Selection(
        string="State",
        selection=[
            ("new", "New"),
            ("offer-received", "Offer Received"),
            ("offer-accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        required=True,
        copy=False,
        default="new",
    )
    property_type_id = fields.Many2one("estate.property.type")
    buyer_id = fields.Many2one("res.partner", copy=False)
    seller_id = fields.Many2one(
        "res.users", name="Salesperson", default=lambda self: self.env.user
    )
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many(
        "estate.property.offer", "property_id", string="Offers"
    )
    best_price = fields.Float(
        compute="_compute_best_price", readonly=True, string="Best Offer"
    )

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for single_property in self:
            single_property.total_area = (
                single_property.living_area + single_property.garden_area
            )

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for single_property in self:
            single_property.best_price = max(single_property.offer_ids.mapped("price"), default=0)

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = None

    def action_property_cancel(self):
        for single_property in self:
            if single_property.state == "sold":
                raise UserError(_("Sold properties cannot be cancelled!"))
            single_property.state = "cancelled"
        return True

    def action_property_sold(self):
        for single_property in self:
            if single_property.state == "cancelled":
                raise UserError(_("Cancelled properties cannot be sold!"))
            single_property.state = "sold"
        return True

    @api.constrains("selling_price", "expected_price")
    def check_selling_price_in_range(self):
        for single_property in self:
            if not float_utils.float_is_zero(single_property.selling_price, precision_rounding=0.1):
                if single_property.selling_price < (0.9 * single_property.expected_price):
                    raise ValidationError(_("Selling price cannot be lower than 90%% of Expected price"))
        return True

    @api.ondelete(at_uninstall=False)
    def _unlink_check_property_state(self):
        for single_property in self:
            if single_property.state not in ["new", "cancelled"]:
                raise UserError(_("Property cannot be deleted unless it is new or cancelled"))
        return True
