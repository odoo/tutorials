import random
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "A real estate property"

    name = fields.Char(string="Property Name", required=True)
    description = fields.Text(string="Estate Description")
    active = fields.Boolean(default=True)

    state = fields.Selection(
        selection=[
            ("new", "New"),
            ("offer received", "Offer Received"),
            ("offer accepted", "Offer accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        default="new",
        string="State",
        required=True,
        copy=False,
    )

    postcode = fields.Char()

    def _three_month_from_now(self):
        """Return as ORM date compliant value three month from today"""

        return fields.Date.today(self) + relativedelta(months=3)

    date_availability = fields.Date(string="Available From", copy=False, default=_three_month_from_now)

    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False, compute="_compute_selling_price")
    bedrooms = fields.Integer(default=random.randint(2, 6))
    facades = fields.Integer()
    living_area = fields.Integer()
    garden_area = fields.Integer()

    garage = fields.Boolean()
    garden = fields.Boolean()

    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
            ("north", "North"),
            ("east", "East"),
            ("south", "South"),
            ("west", "West"),
        ],
    )

    # Related fields
    property_type_id = fields.Many2one("estate.property.type", string="Type")
    property_type_test_value = fields.Char(
        string="Test Value",
        related="property_type_id.test_value",
        readonly=True,
    )

    property_tag_ids = fields.Many2many("estate.property.tag", string="Tag")

    property_offer_ids = fields.One2many(
        comodel_name="estate.property.offer",
        inverse_name="property_id",
        string="Offers",
    )

    # Related fields RES

    partner_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    user_id = fields.Many2one("res.users", string="Salesperson", default=lambda self: self.env.user)

    # Computed Fields
    total_area = fields.Integer(compute="_compute_total_area")

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    best_offer = fields.Float(compute="_compute_best_offer")

    @api.depends('property_offer_ids.price')
    def _compute_best_offer(self):
        for record in self:
            record.best_offer = max((offer.price for offer in record.property_offer_ids), default=0)

    @api.depends('property_offer_ids.status')
    def _compute_selling_price(self):
        for record in self:
            accepted_offers = [offer for offer in record.property_offer_ids if offer.status == "accepted"]

            if len(accepted_offers) > 1:
                raise UserError("Can't accept more then one offer")

            elif accepted_offers:
                record.selling_price = accepted_offers[0].price
                record.state = "offer accepted"
                record.partner_id = accepted_offers[0].partner_id
            else:
                record.selling_price = False
                record.state = "new" if not record.property_offer_ids else "offer received"
                record.partner_id = False

    # Constraining on state instead of selling price because selling price is not a writable field
    @api.constrains("state", "expected_price")
    def _onchange_price(self):
        if not float_is_zero(self.selling_price, 10) and self.selling_price < 0.9 * self.expected_price:
            raise ValidationError("Selling price can't be lower then 0.9 * expected price")

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    def action_cancel_listing(self):
        for record in self:
            if record.state == "sold":
                raise UserError("This listing is already sold and can't be cancelled")
            record.state = "cancelled"
        return True

    def action_sell_listing(self):
        for record in self:
            if record.state == "cancelled":
                raise UserError("This listing is already cancelled and can't be sold")
            record.state = "sold"
        return True

    _sql_constraints = [
        ('unique_name', 'UNIQUE(name)', 'Property name should be unique'),
        ('positive_expected_price', 'CHECK(expected_price >= 0)', 'Expected price should be > 0'),
    ]
