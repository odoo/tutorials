from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    _order = "id desc"

    estate_property_type_id = fields.Many2one(comodel_name="estate.property.type", ondelete="set null")

    estate_property_tag_ids = fields.Many2many(comodel_name="estate.property.tag")

    buyer_id = fields.Many2one(comodel_name="res.partner", ondelete="set null")

    seller_id = fields.Many2one(comodel_name="res.users", ondelete="set null",
                                default=lambda self: self.env.user.id)

    estate_property_offer_ids = fields.One2many(comodel_name="estate.property.offer", inverse_name="estate_property_id",
                                                copy=False)

    name = fields.Char(string="Estate Property", required=True)

    active = fields.Boolean(default=True)

    description = fields.Text(string="Description")

    postcode = fields.Char(string="Postcode")

    status = fields.Selection(
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        default="new",
    )

    date_availability = fields.Date(
        string="Available From",
        default=fields.Date.today() + relativedelta(months=+3),
        copy=False,
    )

    expected_price = fields.Float(string="Expected Price", required=True)

    selling_price = fields.Float(string="Selling Price", copy=False, readonly=True)

    bedrooms = fields.Integer(string="Bedrooms", default=2)

    living_area = fields.Integer(string="Living Area (sqm)")

    facades = fields.Integer(string="Facades")

    garage = fields.Boolean(string="Garage", default=False)

    garden = fields.Boolean(string="Garden", default=False)
    garden_area = fields.Integer(string="Garden Area")
    garden_orientation = fields.Selection(
        selection=[("north", "North"), ("east", "East"), ("south", "South"), ("west", "West")],
    )

    total_area = fields.Integer(compute="_compute_total_area")

    best_price = fields.Float(string="Best Offer", compute="_compute_best_price")

    _check_expected_price_positive = models.Constraint(
        definition="CHECK(expected_price > 0)",
        message="expected_price <= 0",
    )

    _check_selling_price_positive = models.Constraint(
        definition="CHECK(selling_price is null or selling_price > 0)",
        message="selling_price <= 0",
    )

    @api.depends("living_area")
    def _compute_total_area(self):
        for estate in self:
            estate.total_area = estate.living_area + estate.garden_area

    @api.depends("estate_property_offer_ids")
    def _compute_best_price(self):
        for estate in self:
            estate.best_price = max(estate.mapped('estate_property_offer_ids.price') or [0])

    @api.constrains('selling_price')
    def _check_ninety_percent_of_expected(self):
        for estate in self:
            if estate.selling_price > 0:
                if float_compare(estate.selling_price, 0.9 * estate.expected_price, 2) < 0:
                    raise ValidationError(self.env._("Offer is less than 90% of expected"))

    @api.onchange("garden")
    def _onchange_garden_orientation(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = None

    @api.ondelete(at_uninstall=False)
    def _unlink_if_new_cancelled(self):
        for user in self:
            if user.status not in ("new", "cancelled"):
                raise UserError(self.env._("Cannot delete active listing"))

    def action_set_sold(self):
        self.ensure_one()
        if (not self.active) or self.status == "cancelled":
            raise UserError(self.env._("Cannot set inactive/cancelled listing to sold"))

        offer_accepted = False
        for offer in self.estate_property_offer_ids:
            if offer.status == "accepted":
                offer_accepted = True
                break

        if not offer_accepted:
            raise UserError(self.env._("Cannot sell something without accepted offer"))

        self.status = "sold"
        return True

    def action_set_cancelled(self):
        self.ensure_one()
        if self.status == "sold":
            raise UserError(self.env._("Cannot set sold listing to cancelled"))
        self.status = "cancelled"
        return True

    def action_uncancel(self):
        self.ensure_one()
        self.status = "new"
        return True

    def set_offer_received(self):
        for estate in self:
            estate.status = "offer_received"
