from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        copy=False, default=lambda self: fields.Date.add(fields.Date.today(), months=3)
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
        ],
        string="Garden Orientation",
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("canceled", "Canceled"),
        ],
        copy=False,
        default="new",
        required=True,
    )
    property_type_id = fields.Many2one("estate.property.type", string="Type")
    seller_id = fields.Many2one(
        "res.users",
        string="Sales Person",
        default=lambda self: self.env.user,
    )
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many(
        "estate.property.offer",
        "property_id",
        string="Offers",
    )
    total_area = fields.Integer(compute="_compute_total_area", string="Total Area")

    def action_sold(self):
        for record in self:
            if record.state == "canceled":
                raise UserError("A canceled property cannot be sold.")
            if not record.offer_ids.filtered(lambda offer: offer.status == "accepted"):
                raise UserError("At lest one of the offer must be accpeted before sold")
            record.state = "sold"

    def action_cancel(self):
        for record in self:
            if record.state == "sold":
                raise UserError("A sold property cannot be canceled.")
            record.state = "canceled"

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    best_price = fields.Float(compute="_compute_best_price", string="Best Offer")

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped("price"), default=0.0)

    @api.onchange("garden")
    def _onchange_garden(self):
        for record in self:
            if record.garden:
                record.garden_area = 10
                record.garden_orientation = "north"
            else:
                record.garden_area = False
                record.garden_orientation = False

    _check_expected_price = models.Constraint(
        "CHECK(expected_price > 0)",
        "The expected price must be strictly positive.",
    )

    _check_selling_price = models.Constraint(
        "CHECK(selling_price > 0)",
        "The selling price must be strictly positive.",
    )

    @api.constrains("selling_price", "expected_price")
    def _check_selling_price(self):
        for record in self:
            if float_is_zero(record.selling_price, precision_rounding=0.01):
                continue
            if (
                float_compare(
                    record.selling_price,
                    record.expected_price * 0.9,
                    precision_rounding=0.01,
                )
                < 0
            ):
                raise ValidationError(
                    "The selling price cannot be lower than 90% of the expected price."
                )
