from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError, RedirectWarning
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real state Property"
    _order = "id desc"
    _inherits = {"estate.property.address": "address_id"}

    address_id = fields.Many2one(
        "estate.property.address", required=True, ondelete="cascade"
    )
    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Integer()
    date_availability = fields.Date(
        default=lambda self: fields.Date.today() + relativedelta(months=3), copy=False
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string="Garden Area(sqm)")
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
        [
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        required=True,
        copy=False,
        default="new",
    )
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    buyer_id = fields.Many2one(
        "res.partner",
        string="Buyer",
        copy=False,
    )
    seller_id = fields.Many2one(
        "res.users", string="Seller", default=lambda self: self.env.user
    )
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many(
        "estate.property.offer",
        "property_id",
        string="Offers",
    )
    total_area = fields.Integer(compute="_compute_total_area", store=True)
    best_price = fields.Float(compute="_compute_best_price", store=True)
    offer_counts = fields.Integer(compute="_compute_offer_counts", store=True)

    _check_expected_price = models.Constraint(
        "CHECK(expected_price > 0)",
        "Expected price must be positive!",
    )

    @api.constrains("selling_price", "expected_price")
    def _check_selling_price(self):
        for record in self:
            if float_is_zero(record.selling_price, precision_digits=2):
                continue
            min_selling_price = record.expected_price * 0.9
            if (
                float_compare(
                    record.selling_price, min_selling_price, precision_digits=2
                )
                < 0
            ):
                raise ValidationError(
                    _("The selling price must be at least 90% of the expected price.")
                )

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped("price"), default=0.0)

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    @api.depends("offer_ids")
    def _compute_offer_counts(self):
        for record in self:
            record.offer_counts = len(record.offer_ids)

    @api.ondelete(at_uninstall=False)
    def _unlink_if_delete_property(self):
        for record in self:
            if record.state in ("offer_received", "offer_accepted", "sold"):
                raise UserError(_("you can not delete a property!"))

    def action_cancelled(self):
        sold_properties = self.filtered(lambda r: r.state == "sold")
        if sold_properties:
            raise RedirectWarning(
                _(
                    "A sold property cannot be cancelled",
                    self.env.ref("estate.estate_property_offer_action").id,
                    "go to offer page!",
                )
            )
            self.state = "cancelled"

    def action_sold(self):
        cancel_properties = self.filtered(lambda r: r.state == "cancelled")
        if cancel_properties:
            raise UserError(_("A cancelled property cannot be sold"))
        accepted_offer = self.offer_ids.filtered(
            lambda offer: offer.status == "accepted"
        )
        if not accepted_offer:
            raise UserError(_("Property can not be sold without an accepted offer"))
        self.state = "sold"
