from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property Module"
    _order = "id desc"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        default=fields.Date.add(fields.Date.today(), months=3),
        copy=False,
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_areas = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        [("north", "North"), ("south", "South"), ("east", "East"), ("west", "West")],
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        [
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        default="new",
        required=True,
        copy=False,
    )
    property_type_id = fields.Many2one("estate.property.type")
    buyer_id = fields.Many2one("res.partner", copy=False)
    seller_id = fields.Many2one("res.users", default=lambda self: self.env.user)
    property_tag_ids = fields.Many2many("estate.property.tag")
    offer_ids = fields.One2many("estate.property.offer", "property_id")
    total_area = fields.Integer(compute="_compute_total_area")
    best_price = fields.Float(compute="_compute_best_price")

    _check_expected_price = models.Constraint(
        "CHECK(expected_price > 0)",
        "The expected price must be strictly positive.",
    )
    _check_selling_price = models.Constraint(
        "CHECK(selling_price >= 0)",
        "The selling price must be positive",
    )

    @api.depends("living_areas", "garden_area")
    def _compute_total_area(self):
        for property in self:
            property.total_area = property.garden_area + property.living_areas

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for property in self:
            property.best_price = (
                max(property.offer_ids.mapped("price")) if len(property.offer_ids) > 0 else 0
            )

    @api.constrains("expected_price", "selling_price")
    def _check_selling_price(self):
        for property in self:
            too_low = float_compare(property.selling_price, 0.9 * property.expected_price, 3) == -1
            if not float_is_zero(property.selling_price, 3) and too_low:
                msg = "The selling price cannot be lower than 90 percents of the expected price."
                raise ValidationError(msg)

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = None

    @api.ondelete(at_uninstall=False)
    def _unlink_if_new_or_cancelled_property(self):
        for property in self:
            if property.state != "new" and property.state != "cancelled":
                msg = "Only new or cancelled properties can be deleted"
                raise UserError(msg)
        return super().unlink()

    def action_sold_property(self):
        for property in self:
            if property.state == "cancelled":
                msg = "Sold properties cannot be cancelled"
                raise UserError(msg)
            property.state = "sold"
        return True

    def action_cancel_property(self):
        for property in self:
            if property.state == "sold":
                msg = "Cancelled properties cannot be sold"
                raise UserError(msg)
            property.state = "cancelled"
        return True
