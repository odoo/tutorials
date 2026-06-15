from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    _order = "id desc"

    name = fields.Char(string="Title", required=True)
    active = fields.Boolean(default=True)
    description = fields.Text()
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(
        string="Available From",
        copy=False,
        default=lambda self: fields.Date.today() + relativedelta(months=3),
    )
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(
        string="Selling Price",
        readonly=True,
        copy=False,
    )
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
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
        string="State",
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("canceled", "Canceled"),
        ],
        required=True,
        copy=False,
        default="new",
    )
    property_type_id = fields.Many2one(
        comodel_name="estate.property.type",
        string="Property Type",
    )
    salesman_id = fields.Many2one(
        comodel_name="res.users",
        string="Salesman",
        default=lambda self: self.env.user,
    )
    buyer_id = fields.Many2one(
        comodel_name="res.partner",
        string="Buyer",
        readonly=True,
        copy=False,
    )
    tag_ids = fields.Many2many(
        comodel_name="estate.property.tag",
        string="Tags",
    )
    offer_ids = fields.One2many(
        comodel_name="estate.property.offer",
        inverse_name="property_id",
        string="Offers",
    )
    total_area = fields.Integer(
        string="Total Area (sqm)",
        compute="_compute_total_area",
    )
    best_price = fields.Float(
        string="Best Offer",
        compute="_compute_best_price",
    )

    _check_expected_price_positive = models.Constraint(
        "CHECK(expected_price > 0)",
        "A property expected price should be strictly positive.",
    )
    _check_selling_price_positive = models.Constraint(
        "CHECK(selling_price >= 0)",
        "A property selling price should be positive.",
    )

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for property_ in self:
            property_.total_area = property_.living_area + property_.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for property_ in self:
            property_.best_price = max(property_.offer_ids.mapped("price"), default=0.0)

    @api.constrains("selling_price", "expected_price")
    def _check_selling_price(self):
        for property_ in self:
            if float_is_zero(property_.selling_price, precision_digits=2):
                continue

            minimum_price = property_.expected_price * 0.9
            if (
                float_compare(
                    property_.selling_price,
                    minimum_price,
                    precision_digits=2,
                )
                < 0
            ):
                raise ValidationError(
                    self.env._(
                        "The selling price must be at least 90%% of the expected "
                        "price. You must reduce the expected price if you want to "
                        "accept this offer."
                    )
                )

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    @api.ondelete(at_uninstall=False)
    def _prevent_unlink_not_new_or_canceled(self):
        for property_ in self:
            if property_.state not in ("new", "canceled"):
                raise UserError(
                    self.env._("Only new or canceled properties can be deleted.")
                )

    def action_sold(self):
        self.ensure_one()

        if self.state == "canceled":
            raise UserError(self.env._("Canceled properties cannot be sold."))

        self.state = "sold"
        return True

    def action_cancel(self):
        self.ensure_one()

        if self.state == "sold":
            raise UserError(self.env._("Sold properties cannot be canceled."))

        self.state = "canceled"
        return True
