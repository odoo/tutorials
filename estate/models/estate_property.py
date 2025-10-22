from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare
from dateutil.relativedelta import relativedelta


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"

    name = fields.Char(required=True, string="Title")
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        string="Available From",
        copy=False,
        default=lambda self: fields.Date.today() + relativedelta(months=3),
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(copy=False, readonly=True)
    best_price = fields.Float(string="Best Offer", compute="_compute_best_price")
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living Area(sqm)")
    total_area = fields.Integer(string="Total Area(sqm)", compute="_compute_total_area")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ]
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        default="new",
        required=True,
    )
    salesman_id = fields.Many2one(
        "res.users",
        string="Salesman",
        default=lambda self: self.env.user.id,
    )
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    property_type_id = fields.Many2one(
        "estate.property.type", string="Property Type", copy=False
    )
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")

    _sql_constraints = [
        (
            "check_positive_expected",
            "CHECK(expected_price >= 0)",
            "Expected Price must be positive value.",
        ),
        (
            "check_positive_selling",
            "CHECK(selling_price >= 0)",
            "Selling Price must be positive value.",
        ),
        (
            "check_positive_offer",
            "CHECK(best_price >= 0)",
            "Offer Price must be positive value.",
        ),
    ]

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for rec in self:
            rec.best_price = 0
            if rec.offer_ids:
                rec.best_price = max(rec.offer_ids.mapped("price"))

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for rec in self:
            rec.total_area = rec.living_area + rec.garden_area

    @api.onchange("garden")
    def _onchange_partner_id(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    @api.constrains("expected_price", "selling_price")
    def _check_selling_price(self):
        for rec in self:
            expected_price = (rec.expected_price * 90) / 100
            if (
                float_compare(rec.selling_price, expected_price, precision_digits=2) < 0
                and rec.selling_price
            ):
                raise ValidationError(
                    _("Selling price must be atlease 90% of Expected Price.")
                )

    @api.ondelete(at_uninstall=False)
    def _unlink_except_contains_new_cancelled_state(self):
        for rec in self:
            if rec.state in ("new", "cancelled"):
                raise UserError(
                    _("You cannot delete records in new or cancelled state.")
                )

    def action_sell_property(self):
        for rec in self:
            if rec.state == "cancelled":
                raise UserError(_("A Cancelled Property Can not be Sold"))
            rec.state = "sold"

    def action_cancel_property(self):
        for rec in self:
            if rec.state == "sold":
                raise UserError(_("A Sold Property Can not be Cancelled"))
            rec.state = "cancelled"
