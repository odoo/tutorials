from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class Property(models.Model):
    _name = "estate.property"
    _description = "Estate property"
    _order = "id desc"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        copy=False,
        default=lambda self: fields.Date.add(
            fields.Date.today(),
            months=3,
        ),
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer()
    has_garage = fields.Boolean()
    has_garden = fields.Boolean()
    garden_area = fields.Integer(string="Garden Area (sqm)")
    total_area = fields.Integer(compute="_compute_total_area", string="Total Area (sqm)")
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        string="State",
        selection=[
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
    type_id = fields.Many2one("estate.property.type")
    partner_id = fields.Many2one(
        "res.partner",
        string="Buyer",
        copy=False,
    )
    user_id = fields.Many2one(
        "res.users",
        string="Salesperson",
        index=True,
        default=lambda self: self.env.user,
    )
    tag_ids = fields.Many2many("estate.property.tag")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    best_price = fields.Float(compute="_compute_best_price")

    _check_expected_price_positive = models.Constraint(
        "CHECK(expected_price >= 0)",
        "The Expected Price should be positive or zero.",
    )
    _check_selling_price_positive = models.Constraint(
        "CHECK(selling_price > 0)",
        "The Selling Price should be positive.",
    )

    @api.constrains("selling_price")
    def _check_selling_price(self):
        for record in self:
            if not float_is_zero(record.selling_price, 2) and\
                float_compare(record.selling_price, (record.expected_price * 0.9), 2) < 0:
                raise ValidationError(_(r"The selling price cannot be lower than 90% of the expected price"))

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids")
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped("price"))
                if record.state == "new":
                    record.state = "offer_received"
            else:
                record.best_price = 0
                record.state = "new"

    @api.onchange("has_garden")
    def _onchange_has_garden(self):
        for record in self:
            if record.has_garden:
                record.garden_area = 10
                record.garden_orientation = "north"
            else:
                record.garden_area = 0
                record.garden_orientation = False

    def action_cancel_property(self):
        for record in self:
            if record.state == "sold":
                raise UserError(_("A sold property cannot be cancelled"))
            record.state = "cancelled"
        return True

    def action_sell_property(self):
        for record in self:
            if record.state == "cancelled":
                raise UserError(_("A cancelled property cannot be sold"))
            if not ("accepted" in record.offer_ids.mapped("status")):
                raise UserError(_("A offer need to be accepted before selling"))
            record.state = "sold"
        return True
