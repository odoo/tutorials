from dateutil.relativedelta import relativedelta
from datetime import timedelta

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"
    _order = "id desc"
    _inherit = ["mail.thread"]

    name = fields.Char(required=True)

    description = fields.Text()

    postcode = fields.Char()

    date_available = fields.Date(
        default=lambda self: fields.Date.today() + relativedelta(months=3),
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

    garden_area = fields.Integer()

    total = fields.Float(
        compute="_compute_total",
    )

    garden_orientation = fields.Selection(
        [
            ('north', "North"),
            ('south', "South"),
            ('east', "East"),
            ('west', "West"),
        ],
    )

    active = fields.Boolean(default=True)

    state = fields.Selection(
        [
            ('new', "New"),
            ('offer_received', "Offer Received"),
            ('offer_accepted', "Offer Accepted"),
            ('sold', "Sold"),
            ('cancelled', "Cancelled"),
        ],
        default="new",
        required=True,
        copy=False,
        tracking=True,
    )

    buyer_id = fields.Many2one(
        "res.partner",
        string="Buyer",
        copy=False,
    )

    salesperson_id = fields.Many2one(
        "res.users",
        string="Salesperson",
        default=lambda self: self.env.user,
    )

    property_type_id = fields.Many2one(
        "estate.property.type",
        string="Property Type",
    )

    tag_ids = fields.Many2many(
        "estate.property.tag",
        string="Tags",
    )

    offer_ids = fields.One2many(
        "estate.property.offer",
        "property_id",
        string="Offers",
    )

    best_offer = fields.Float(
        string="Best Offer",
        compute="_compute_best_price",
    )

    _check_expected_price = models.Constraint(
        "CHECK(expected_price > 0)",
        "The expected price must be strictly positive.",
    )

    _check_selling_price = models.Constraint(
        "CHECK(selling_price >= 0)",
        "The selling price must be positive.",
    )
    is_suspicious = fields.Boolean(
        compute="_compute_is_suspicious",
        store=True,
    )

    @api.depends("garden_area", "living_area")
    def _compute_total(self):
        for record in self:
            record.total = record.garden_area + record.living_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_offer = max(record.offer_ids.mapped("price"))
            else:
                record.best_offer = 0.0

    @api.constrains("selling_price", "expected_price")
    def _check_seling_price(self):
        for record in self:
            if float_is_zero(record.selling_price, precision_digits=2):
                continue

            if (
                float_compare(
                    record.selling_price,
                    record.expected_price * 0.9,
                    precision_digits=2,
                )
                < 0
            ):
                raise ValidationError(
                    "Selling price cannot be lower than 90% of expected price!",
                )

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = ""

    def action_cancel(self):
        for record in self:
            if record.state == "sold":
                raise UserError("A sold property cannot be cancelled")

            record.state = "cancelled"

        return True

    def action_sold(self):
        for record in self:
            if record.state == "cancelled":
                raise UserError("A cancelled property can't be sold")

            record.state = "sold"

        return True

    @api.ondelete(at_uninstall=False)
    def ondelete(self):
        for record in self:
            if record.state != "new" or record.state != "cancelled":
                raise UserError("This property can't be deleted")

    @api.depends("offer_ids", "offer_ids.partner_id", "offer_ids.create_date")
    def _compute_is_suspicious(self):
        now = fields.Datetime.now()
        five_minutes_ago = now - timedelta(minutes=5)

        Offer = self.env["estate.property.offer"]

        for property_record in self:
            property_record.is_suspicious = False

            partners = property_record.offer_ids.mapped("partner_id")

            for partner in partners:
                offer_count = Offer.search_count(
                    [
                        ("partner_id", "=", partner.id),
                        ("property_id", "=", property_record.id),
                        ("create_date", ">=", five_minutes_ago),
                    ]
                )

                if offer_count >= 2:
                    property_record.is_suspicious = True
                    break
