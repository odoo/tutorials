from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstatePropertyModel(models.Model):
    _name = "estate.property"
    _description = "Defines the model of a real estate property"
    _order = "id desc"

    name = fields.Char(required=True, string="Title")
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        string="Date of availability",
        copy=False,
        default=fields.Date.add(fields.Date.today(), months=3),
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(string="Number of bedrooms", default=2)
    living_area = fields.Integer()
    facades = fields.Integer(string="Number of facades")
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        [
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
        string="Garden orientation",
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        [
            ("new", "New"),
            ("offer_received", "Offer received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        required=True,
        copy=False,
        default="new",
    )
    state_active = fields.Boolean(compute="_compute_state_active")
    offers_readonly = fields.Boolean(compute="_compute_offers_readonly")

    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    sales_person_id = fields.Many2one(
        "res.users",
        string="Salesperson",
        default=lambda self: self.env.user,
    )
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    total_area = fields.Integer(string="Total area", compute="_compute_total_area")
    best_offer = fields.Float(string="Best offer", compute="_compute_best_offer")

    @api.depends("offer_ids.status")
    def _compute_offers_readonly(self):
        readonly_offers_states = ("sold", "cancelled", "offer_accepted")
        for estate_property in self:
            estate_property.offers_readonly = estate_property.state in readonly_offers_states

    @api.depends("state")
    def _compute_state_active(self):
        readonly_states = ("sold", "cancelled")
        for estate_property in self:
            estate_property.state_active = estate_property.state not in readonly_states

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for estate_property in self:
            estate_property.total_area = estate_property.living_area + estate_property.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_offer(self):
        for estate_property in self:
            estate_property.best_offer = max(estate_property.offer_ids.mapped("price"), default=0.0)

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = None
            self.garden_orientation = None

    def action_sell_property(self):
        if any(estate_property.state == "cancelled" for estate_property in self):
            raise UserError("Cannot sell a cancelled property")
        self.state = "sold"
        return True

    def action_cancel_property(self):
        if any(estate_property.state == "sold" for estate_property in self):
            raise UserError("Cannot cancel a sold property")
        self.state = "cancelled"
        return True

    @api.constrains("selling_price", "expected_price")
    def _check_selling_price(self):
        for estate_property in self:
            if (
                not float_is_zero(estate_property.selling_price, precision_rounding=0.01)
                and float_compare(
                    estate_property.selling_price,
                    estate_property.expected_price * 0.9,
                    precision_rounding=0.01,
                )
                == -1
            ):
                raise ValidationError(
                    "The selling price cannot be lower than 90% of the expected price."
                )

    _sql_constraints = [
        (
            "check_expected_price_positive",
            "CHECK(expected_price > 0)",
            "The expected price must be strictly positive.",
        ),
        (
            "check_selling_price_positive",
            "CHECK(selling_price >= 0)",
            "The selling price must be positive.",
        ),
    ]
