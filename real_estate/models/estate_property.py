from odoo import api, fields, models
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "This is a real estate module"
    _order = "id desc"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    active = fields.Boolean(default=True)
    buyer_id = fields.Many2one(comodel_name="res.partner", string="Buyer", copy=False)
    total_area = fields.Float(compute="_compute_total_area", string="Total Area")
    best_offer = fields.Float(compute="_compute_best_price", string="Best Offer")
    date_availability = fields.Date(
        string="Availability From",
        default=lambda self: fields.Date.today() + relativedelta(months=3),
        copy=False,
    )
    estate_property_offer_ids = fields.One2many(
        comodel_name="estate.property.offers",
        inverse_name="property_id",
        string="Offers",
    )
    seller_id = fields.Many2one(
        comodel_name="res.users",
        string="SalesPerson",
        default=lambda self: self.env.user,
    )
    estate_property_type_id = fields.Many2one(
        comodel_name="estate.property.types", string="Property Type"
    )
    estate_property_tag_ids = fields.Many2many(
        comodel_name="estate.property.tags", string="Tags"
    )
    garden_orientation = fields.Selection(
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ]
    )
    state = fields.Selection(
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        copy=False,
        required=True,
        default="new",
    )

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("estate_property_offer_ids")
    def _compute_best_price(self):
        for record in self:
            prices = record.estate_property_offer_ids.mapped("price")
            record.best_offer = max(prices) if prices else 0.0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    def action_sold(self):
        for record in self:
            if not record.state == "offer_accepted":
                raise UserError("Accept an offer first")

            if record.state == "cancelled":
                raise UserError("You cannot mark a cancelled property as sold.")
            record.state = "sold"

    def action_cancel(self):
        for record in self:
            if record.state == "sold":
                raise UserError("You cannot mark a sold property as cancelled.")
            record.state = "cancelled"

    _sql_constraints = [
        (
            "check_expected_price_positive",
            "CHECK(expected_price > 0)",
            "Expected price must be strictly positive.",
        ),
    ]

    @api.constrains("expected_price", "selling_price")
    def _check_selling_price(self):
        for record in self:
            if float_is_zero(record.selling_price, precision_digits=2):
                continue

            min_price = record.expected_price * 0.9
            if float_compare(record.selling_price, min_price, precision_digits=2) < 0:
                raise ValidationError(
                    "Selling price must be at least 90% of the expected price."
                )

    @api.ondelete(at_uninstall=False)
    def _check_deletion_state(self):
        for rec in self:
            if rec.state not in ["new", "cancelled"]:
                raise UserError(
                    "Only properties in 'New' or 'Cancelled' state can be deleted."
                )
