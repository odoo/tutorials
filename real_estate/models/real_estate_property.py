from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"
    _order = "id desc"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        copy=False, default=lambda self: fields.Date.today() + relativedelta(months=3)
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(
        readonly=True,
        copy=False,
    )
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(
        compute="_compute_garden_defaults", store=True, readonly=False
    )
    garden_orientation = fields.Selection(
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
        help="Garden facing direction",
        compute="_compute_garden_defaults",
        store=True,
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        string="States",
        selection=[
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
    property_type_id = fields.Many2one("estate.property.type")
    buyer_id = fields.Many2one("res.partner", copy=False)
    salesperson_id = fields.Many2one(
        "res.users", string="Sales Person", default=lambda self: self.env.user
    )
    tag_ids = fields.Many2many("estate.property.tag")
    offer_ids = fields.One2many("estate.property.offer", "property_id")
    total_area = fields.Float(compute="_compute_total_area")
    best_price = fields.Float(compute="_compute_best_price")

    _check_expected_price = models.Constraint(
        "CHECK(expected_price > 0)", "Expected price Must be positive"
    )

    _check_selling_price = models.Constraint(
        "CHECK(selling_price >= 0)", "Selling Price Must be Positive"
    )

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            if not record.mapped("offer_ids.price"):
                record.best_price = 0
            else:
                record.best_price = max(record.mapped("offer_ids.price"))

    @api.depends("garden")
    def _compute_garden_defaults(self):
        for record in self:
            if record.garden:
                record.garden_area = 10
                record.garden_orientation = "north"
            else:
                record.garden_area = 0
                record.garden_orientation = False

    def _check_expected_selling_price(self):
        for record in self:
            if float_is_zero(record.selling_price, precision_digits=2):
                continue

            expected_selling_price = record.expected_price * 0.9
            if (float_compare(record.selling_price, expected_selling_price, precision_digits=2) < 0):
                raise ValidationError(
                    _("Selling price Must be 90% of the expected price")
                )

    @api.ondelete(at_uninstall=False)
    def _unlink_if_new_or_cancelled(self):
        for record in self:
            if record.state not in ["new", "cancelled"]:
                raise UserError(
                    _(
                        "Can not delete this property as it's state is neither New nor cancelled"
                    )
                )

    def action_sold(self):
        self.ensure_one()
        if self.filtered(lambda r: r.state == "cancelled"):
            raise UserError(_("Cancelled Properties Can Not be sold"))
        if not self.buyer_id:
            raise UserError(_("Cannot sell a property with no buyer"))
        self.state = "sold"
        return {
            "effect": {
                "fadeout": "slow",
                "message": "Congratulation This property mark as sold",
                "type": "rainbow_man",
            }
        }

    def action_cancelled(self):
        self.ensure_one()
        if self.filtered(lambda r: r.state == "sold"):
            raise UserError(_("Sold Properties can not be cancel"))
        self.state = "cancelled"
        return True

    def action_approve_best_offer(self):
        for record in self:
            if "accepted" in record.offer_ids.mapped("status"):
                continue
            if record.filtered(lambda r: r.state == "sold"):
                raise UserError(_("Sold properties cannot accept other Offers."))
            target_offer = record.offer_ids.filtered(
                lambda r: r.price == record.best_price
            )
            if target_offer:
                target_offer = target_offer[0]
                target_offer.status = "accepted"
            (record.offer_ids - target_offer).status = "refused"
            record.selling_price = target_offer.price
            record.buyer_id = target_offer.partner_id
            record.state = "offer_accepted"
