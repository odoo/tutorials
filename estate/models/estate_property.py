from datetime import date
from dateutil.relativedelta import relativedelta

from odoo import api, _, exceptions, fields, models
from odoo.orm.utils import ValidationError
from odoo.tools import float_compare


class EstateProperty(models.Model):
    _name = "realestate.properties"
    _description = "Real estate properties"
    _order = "id desc"

    active = fields.Boolean(default=True)
    name = fields.Char("Title", required=True, translate=True)
    description = fields.Text("Notes")
    postcode = fields.Char("Postcode", required=True)
    date_availability = fields.Date(
        "Availability date",
        copy=False,
        default=date.today() + relativedelta(months=3),
    )
    expected_price = fields.Float("Expected Price", required=True)
    _check_expected_price = models.Constraint(
        "CHECK(expected_price > 0)",
        _("The expected price should be strictly positive"),
    )
    selling_price = fields.Float(
        "Selling price",
        copy=False,
        readonly=True,
        compute="_compute_selling_price",
    )
    _check_selling_price = models.Constraint(
        "CHECK(selling_price >= 0)",
        _("The selling price should be strictly positive"),
    )
    state = fields.Selection(
        [
            ("new", "New"),
            ("offer received", "Offer Received"),
            ("offer accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        default="new",
        required=True,
        copy=False,
    )
    bedrooms = fields.Integer("Bedrooms", default=2)
    facades = fields.Integer("Facades")
    garage = fields.Boolean("Garage")
    garden = fields.Boolean("Garden")
    living_area = fields.Integer("Living area (sqm)")
    garden_area = fields.Integer("Garden area (sqm)")
    total_area = fields.Integer("Total area (sqm)", compute="_compute_total_area")
    garden_orientation = fields.Selection(
        [
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
    )
    best_offer = fields.Float("Best Offer", compute="_compute_best_price")
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    sale_rep_id = fields.Many2one(
        "res.users",
        string="Salesperson",
        default=lambda self: self.env.user,
    )
    property_type_id = fields.Many2one("realestate.properties.type")
    property_tag_ids = fields.Many2many("realestate.properties.tag", string="Tags")
    offer_ids = fields.One2many(
        "realestate.properties.offer",
        "property_id",
    )

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            prices = record.offer_ids.mapped("price")
            record.best_offer = max(prices, default=0)

    @api.depends("offer_ids")
    def _compute_selling_price(self):
        for record in self:
            accepted_offer = record.offer_ids.filtered(lambda o: o.status == "accepted")
            record.selling_price = accepted_offer.price if accepted_offer else 0.0

    @api.onchange("offer_ids")
    def _onchange_offer(self):
        for record in self:
            # in case of a delete
            if len(record.offer_ids) == 0:
                record.state = "new"

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = None

    def sold_action_btn(self):
        for record in self:
            if record.state == "cancelled":
                raise exceptions.UserError(_("Cancelled properties cannot be sold."))

            record.state = "sold"

    def cancelled_action_btn(self):
        for record in self:
            if record.state == "sold":
                raise exceptions.UserError(_("Sold properties cannot be cancelled."))
            record.state = "cancelled"

    @api.constrains("expected_price", "selling_price")
    def _check_offer_acceptable_price(self):
        for record in self:
            if (
                record.state == "offer accepted"
                and float_compare(record.selling_price, record.expected_price * 0.9, 3)
                <= 0
            ):
                raise ValidationError(
                    _(
                        "The selling price should be greater than 90% of the expected price.",
                    ),
                )

    @api.ondelete(at_uninstall=False)
    def _unlink_except_state_is_new_or_cancelled(self):
        for record in self:
            if record.state in ("new", "cancelled"):
                raise exceptions.UserError(
                    _("Property that is either new or cancelled, can't be deleted."),
                )
