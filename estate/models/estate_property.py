from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property Options"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        copy=False,
        default=lambda x: fields.Datetime.add(fields.Datetime.today(), months=3),
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer()
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
    user_id = fields.Many2one(
        comodel_name="res.users",
        string="Salesperson",
        default=lambda self: self.env.user,
    )
    partner_id = fields.Many2one(comodel_name="res.partner", string="Buyer", copy=False)
    property_tag_ids = fields.Many2many(comodel_name="estate.property.tag")
    property_offer_ids = fields.One2many("estate.property.offer", "property_id")

    total_area = fields.Integer(compute="_compute_total_area")
    best_price = fields.Float(compute="_compute_best_price")

    _sql_constraints = [
        (
            "check_expected_price",
            "CHECK(expected_price >= 0)",
            "Property expected price MUST be postive.",
        ),
        (
            "check_selling_price",
            "CHECK(selling_price >= 0)",
            "Property selling price MUST be postive.",
        ),
    ]

    @api.constrains("expected_price", "selling_price")
    def _check_selling_price(self):
        for record in self:
            if float_is_zero(record.selling_price, precision_digits=2):
                continue
            if (
                float_compare(
                    value1=record.selling_price,
                    value2=(0.9 * record.expected_price),
                    precision_digits=2,
                )
                == -1
            ):
                raise ValidationError(
                    "Property selling price  MUST be 90% at least of the expected price."
                )

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("property_offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(
                record.property_offer_ids.mapped("price"), default=0
            )

    @api.onchange("garden")
    def _onchange_garden(self):
        self.garden_area = 10 if self.garden else 0
        self.garden_orientation = "north" if self.garden else ""

    def action_set_cancelled(self):
        self.ensure_one()
        if self.state == "cancelled":
            raise UserError("Cancelled Items cannot be sold.")
        self.state = "sold"

    def action_set_sold(self):
        for record in self:
            if record.state == "sold":
                raise UserError("Sold Items cannot be cancelled.")
            record.state = "cancelled"

    def action_process_accept(self, offer):
        self.ensure_one()
        if self.state == "offer_accepted":
            raise UserError("this property has already an accepted offer!!")
        self.state = "offer_accepted"
        self.selling_price = offer.price
        self.partner_id = offer.partner_id
