from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    _order = "sequence, id desc"

    name = fields.Char("Title", required=True)
    sequence = fields.Integer(default=1)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        "Available From", default=lambda self: fields.Date.today() + relativedelta(months=3), copy=False
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer("Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer("Garden Area (sqm)")
    garden_orientation = fields.Selection([("north", "North"), ("south", "South"), ("east", "East"), ("west", "West")])
    active = fields.Boolean(default=True)
    state = fields.Selection(
        [
            ("new", "New"),
            ("offer", "Offer Received"),
            ("accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("canceled", "Cancelled"),
        ],
        default="new",
        readonly=True,
    )
    property_type_id = fields.Many2one("estate.property.type")
    salesman_id = fields.Many2one("res.users", copy=False, default=lambda self: self.env.user)
    buyer_id = fields.Many2one("res.partner", copy=False, readonly=True)
    tag_ids = fields.Many2many("estate.property.tag")
    offer_ids = fields.One2many("estate.property.offer", "property_id")
    total_area = fields.Integer("Total Area (sqm)", compute="_compute_total_area")
    best_offer = fields.Float(compute="_compute_best_offer")

    _check_expected_price = models.Constraint("CHECK(expected_price>0)", "The expected price needs to be bigger then 0")
    _check_selling_price = models.Constraint("CHECK(selling_price>=0)", "The selling price needs to be positive")

    @api.depends("garden_area", "living_area")
    def _compute_total_area(self):
        for estate_property in self:
            estate_property.total_area = estate_property.living_area + estate_property.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_offer(self):
        for estate_property in self:
            estate_property.best_offer = max(estate_property.offer_ids.mapped("price"), default=None)

    @api.onchange("garden")
    def _onchange_garden(self):
        self.garden_area = 10 if self.garden else 0
        self.garden_orientation = "north" if self.garden else None

    @api.constrains("selling_price", "expected_price")
    def _check_selling_price(self):
        for estate_property in self:
            if (
                not float_is_zero(estate_property.selling_price, 2)
                and float_compare(estate_property.selling_price, estate_property.expected_price * 0.9, 2) < 0
            ):
                raise ValidationError("The property can not be sold for a price lower than 90% of the expected price")

    @api.ondelete(at_uninstall=False)
    def _unlink_property(self):
        if any(estate_property.state not in ["new", "canceled"] for estate_property in self):
            raise UserError("Only properties with state new or canceled can be removed!")

    def action_state_to_sold(self):
        self.ensure_one()
        if self.state == "canceled":
            raise UserError("Canceled properties can not be sold")
        if not [offer for offer in self.offer_ids if offer.status == 'accepted']:
            raise UserError("Properties can not be marked as sold if there is no accepted offer")
        self.state = "sold"

    def action_state_to_canceled(self):
        self.ensure_one()
        if self.state == "sold":
            raise UserError("Sold properties can not be canceled")
        self.state = "canceled"

    def accept_offer(self, price, buyer):
        self.ensure_one()
        if self.state not in ["new", "offer"]:
            raise UserError(
                "An offer can can only be accepted when the building is still for sale and no other offer is already accepted"
            )
        self.selling_price = price
        self.buyer_id = buyer
        self.state = "accepted"

    def offer_made(self, price):
        self.ensure_one()
        if self.state not in ["new", "offer"]:
            raise UserError(
                "An offer can can only be accepted when the building is still for sale and no other offer is already accepted"
            )
        if float_compare(price, self.best_offer, 2) <= 0:
            raise UserError("Only offers that are over the current best offer can be accepted")
        self.state = "offer"
