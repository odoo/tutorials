from datetime import timedelta

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property Name"
    _order = "id desc"
    _inherit = ["mail.thread"]

    name = fields.Char("Property name", required=True, size=30)
    postcode = fields.Char("Postcode", size=6, tracking=True)
    date_availability = fields.Date(
        default=fields.Date.today() + timedelta(days=90), copy=False
    )
    expected_price = fields.Float("Expected price", required=True)
    selling_price = fields.Integer("Selling Price", readonly=True, copy=False)
    description = fields.Char("Property description", size=50)
    bedrooms = fields.Integer("Bedrooms", default=2)
    facades = fields.Integer("facade")
    living_area = fields.Integer("Area(sqm)")
    garage = fields.Boolean("Available", help="Mark if Garage is available")
    garden = fields.Boolean(
        "Garden",
        help="Mark if Garden is Present",
    )
    garden_area = fields.Integer("Garden Area(sqm)", default=0)

    active = fields.Boolean(
        "Active", default=True, help="Mark if you want it as Active"
    )
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
    )
    state = fields.Selection(
        string="Status",
        required=True,
        default="new",
        tracking=True,
        copy=False,
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
    )

    total_area = fields.Float(
        compute="_compute_total_area", string="Total area(sqm)", store=True
    )
    best_price = fields.Float(
        compute="_compute_best_offer", string="Best Offer", store=True
    )
    tags_ids = fields.Many2many("estate.property.tags", string="Tags")
    property_type_id = fields.Many2one("estate.property.types", string="Property Type")
    offer_ids = fields.One2many(
        "estate.property.offer", "property_id", string="Offers", tracking=True
    )
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=True, tracking=True)
    salesman_id = fields.Many2one(
        "res.users", default=lambda self: self.env.user, string="Salesman"
    )
    company_id = fields.Many2one(
        "res.company",
        string="Company",
        required=True,
        default=lambda self: self.env.user.company_id,
    )

    _sql_constraints = [
        (
            "check_expected_price",
            "CHECK(expected_price > 0)",
            "The Expected price should be positive",
        ),
        (
            "check_selling_price",
            "CHECK(selling_price > 0)",
            "The selling price should be positive",
        ),
    ]

    @api.constrains("offer_ids")
    def _check_offer_price(self):
        for record in self:
            for offer in record.offer_ids:
                if offer.price < 0:
                    raise ValidationError("The offer price must be positive")

    @api.constrains("selling_price", "expected_price")
    def _check_selling_price(self):
        for record in self:
            if float_is_zero(record.selling_price, precision_digits=2):
                continue
            if (
                float_compare(
                    record.selling_price,
                    (record.expected_price * 0.9),
                    precision_digits=2,
                )
                < 0
            ):
                raise ValidationError(
                    "The selling price must be at least 90% per of expected price."
                )

    @api.ondelete(at_uninstall=False)
    def _unlink_if_allowed(self):
        for record in self:
            if record.state not in ("new", "cancelled"):
                raise UserError(
                    "Property State with new or canceled can only be deleted"
                )

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_offer(self):
        for record in self:
            record.best_price = (
                max(record.offer_ids.mapped("price")) if record.offer_ids else 0.0
            )

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    def action_set_sold(self):
        for record in self:
            if record.state == "cancelled":
                raise UserError("It cannot be sold once cancelled")
            elif not record.offer_ids.filtered(lambda offer: offer.status == "accepted"):
                raise UserError("No offer is accepted")
            elif record.state != "cancelled":
                record.state = "sold"
            else:
                raise UserError("It is already sold")
        return True

    def action_set_canceled(self):
        for record in self:
            if record.state != "sold":
                record.state = "cancelled"
            elif record.state == "sold":
                raise UserError("It cannot be canceled once sold")
            elif record.state == "cancelled":
                raise UserError("It is already canceled")
        return True
