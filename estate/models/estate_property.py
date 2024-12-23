from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"
    _order = "id desc"
    _sql_constraints = [
        (
            "expected_price",
            "CHECK(expected_price > 0)",
            "The expected price must be strictly positive.",
        ),
        (
            "selling_price",
            "CHECK(selling_price >= 0)",
            "The selling price price must be positive.",
        ),
    ]

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        copy=False,
        default=lambda x: fields.Datetime.add(fields.Datetime.today(), months=3),
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
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ]
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        required=True,
        copy=False,
        default="new",
        selection=[
            ("new", "New"),
            ("offer_received", "Offer received"),
            ("offer_accepted", "Offer accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
    )
    property_type_id = fields.Many2one(comodel_name="estate.property.type")
    buyer_id = fields.Many2one(comodel_name="res.partner", copy=False)
    salesman_id = fields.Many2one(
        comodel_name="res.users", default=lambda self: self.env.user
    )
    tag_ids = fields.Many2many(comodel_name="estate.property.tag")
    offer_ids = fields.One2many(
        comodel_name="estate.property.offer", inverse_name="property_id"
    )
    total_area = fields.Integer(compute="_compute_total_area")
    best_price = fields.Float(compute="_compute_best_price")

    @api.constrains("expected_price", "selling_price")
    def _check_selling_price(self):
        for record in self:
            if float_is_zero(record.selling_price, 4):
                continue
            if float_compare(record.selling_price, record.expected_price * 0.9, 4) < 0:
                raise ValidationError(
                    "The selling price cannot be lower than 90% of the expected price."
                )

    @api.depends("garden_area", "living_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            prices = record.offer_ids.mapped("price")
            record.best_price = max(prices, default=0)

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = ""

    @api.ondelete(at_uninstall=False)
    def _unlink_except_new_cancelled(self):
        if self.filtered(
            lambda property: property.state
            in ("offer_received", "offer_accepted", "sold")
        ):
            raise UserError("You can only delete new and cancelled properties.")

    def action_property_sold(self):
        self.ensure_one()
        if self.state == "cancelled":
            raise UserError("Cancelled properties cannot be sold.")
        if not self.offer_ids.filtered(lambda offer: offer.status == "accepted"):
            raise UserError("Cannot sell a property with no accepted offer on it.")
        self.state = "sold"
        return True

    def action_property_cancelled(self):
        self.ensure_one()
        if self.state == "sold":
            raise UserError("Sold properties cannot be cancelled.")
        self.state = "cancelled"
        return True
