from odoo import models, fields, api, exceptions
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _inherit = ["mail.thread"]
    _description = "Real Estate Property"
    _order = "id desc"

    salesperson_id = fields.Many2one(
        "res.users",
        string="Sales Person",
        default=lambda self: self.env.user,
        required=True,
    )
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    property_type_id = fields.Many2one(
        "estate.property.type", string="Property Type", required=True
    )
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        string="Available From", copy=False, default=lambda self: fields.Date.today()
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    garage = fields.Boolean()
    garden = fields.Boolean()
    living_area = fields.Float(string="Living Area (sqm)")
    garden_area = fields.Float(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        [("north", "North"), ("south", "South"), ("east", "East"), ("west", "West")],
        string="Garden Orientation",
    )
    state = fields.Selection(
        [
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("canceled", "Canceled"),
        ],
        string="Status",
        required=True,
        copy=False,
        default="new",
    )
    total_area = fields.Float(
        string="Total Area (sqm)",
        compute="_compute_total_area",
        store=True,
        help="Sum of living area and garden area",
    )
    best_price = fields.Float(
        string="Best Offer", compute="_compute_best_price", store=True
    )

    _sql_constraints = [
        (
            "check_expected_price_positive",
            "CHECK(expected_price >= 0)",
            "The expected price must be strictly positive.",
        ),
        (
            "check_selling_price_positive",
            "CHECK(selling_price >= 0)",
            "The selling price must be strictly positive.",
        ),
        (
            "check_bedrooms_positive",
            "CHECK(bedrooms >= 0)",
            "The number of bedrooms must be zero or positive.",
        ),
    ]

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for area in self:
            area.total_area = area.living_area + area.garden_area

    @api.onchange("garden")
    def _onchange_garden(self):
        for property in self:
            if property.garden:
                property.garden_area = 10
                property.garden_orientation = "north"
            else:
                property.garden_area = 0
                property.garden_orientation = ""

    @api.depends("offer_ids.offer_price")
    def _compute_best_price(self):
        for property in self:
            property.best_price = max(
                property.offer_ids.mapped("offer_price"), default=0.0
            )

    def action_cancel(self):
        for property in self:
            if property.state == "sold":
                raise UserError("A sold property cannot be cancelled.")
            property.state = "canceled"

    def action_sold(self):
        for property in self:
            if property.state == "canceled":
                raise UserError("A cancelled property cannot be sold.")
            property.state = "sold"

    @api.constrains("selling_price", "expected_price")
    def _check_selling_price(self):
        for record in self:
            if float_is_zero(record.selling_price, precision_digits=2):
                continue
            min_acceptable_price = 0.9 * record.expected_price
            if (
                float_compare(
                    record.selling_price, min_acceptable_price, precision_digits=2
                )
                < 0
            ):
                raise ValidationError(
                    "The selling price cannot be lower than 90% of the expected price."
                )

    @api.ondelete(at_uninstall=False)
    def _check_state_before_delete(self):
        for record in self:
            if record.state not in ("new", "canceled"):
                raise UserError(
                    "You can only delete properties in 'New' or 'Cancelled' state."
                )

    # self is the recordset of estate.property
    # price is the new offer price (offer_price)
    # Collects all the offers for the property and checks if the new offer price is lower than any existing offer
    def check_offer(self, price):
        curr_offers = []
        for property in self:
            for offer in property.offer_ids:
                curr_offers.append(offer.offer_price)
            if curr_offers:
                if price < min(curr_offers):
                    raise exceptions.UserError(
                        "New offer cannot be lower than other offers"
                    )
            property.state = "offer_received"
