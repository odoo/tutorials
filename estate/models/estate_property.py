from datetime import date

from dateutil.relativedelta import relativedelta
from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Store Real Estate Properties"
    _order = "id desc"
    # SQL Constraints
    _sql_constraints = [
        (
            "check_expected_price_positive",
            "CHECK(expected_price > 0)",
            "The expected price must be strictly positive.",
        ),
        (
            "check_selling_price_positive",
            "CHECK(selling_price >= 0)",
            "The selling price must be positive.",
        ),
        ("unique_name", "UNIQUE(name)", "The name must be unique."),
    ]

    name = fields.Char("Estate Name", required=True)
    description = fields.Text(help="Enter the real estate item description")
    postcode = fields.Char("Postcode")
    date_availability = fields.Date(
        "Available From",
        copy=False,
        default=lambda self: date.today() + relativedelta(months=3),
    )
    expected_price = fields.Float(digits="Product Price")
    selling_price = fields.Float(digits="Product Price", copy=False, readonly=True)
    bedrooms = fields.Integer(default=2, help="Number of bedrooms in the property")
    living_area = fields.Integer("Living Area (m²)")
    facades = fields.Integer(help="Number of building facades")
    garage = fields.Boolean(default=False)
    garden = fields.Boolean(default=False)
    garden_area = fields.Integer("Garden Area (m²)")
    garden_orientation = fields.Selection(
        [("north", "North"), ("south", "South"), ("east", "East"), ("west", "West")],
        help="Direction the garden faces",
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
        copy=False,
        default="new",
    )

    note = fields.Text("Special mentions about the house")

    # Relations
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    salesperson_id = fields.Many2one(
        "res.users", string="Salesperson", default=lambda self: self.env.user
    )
    tag_ids = fields.Many2many("estate.property.tag", string="Property Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")

    # Computed fields
    total_area = fields.Float(compute="_compute_total_area")
    best_price = fields.Float(string="Best Offer", compute="_compute_best_price")

    @api.ondelete(at_uninstall=False)
    def _check_can_be_deleted(self):
        for estate in self:
            if estate.state not in ["new", "cancelled"]:
                raise UserError(_("Only 'new' or 'cancelled' properties can be deleted."))

    # Computed functions
    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for estate in self:
            estate.total_area = estate.living_area + estate.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for estate in self:
            prices = estate.offer_ids.mapped("price")
            estate.best_price = max(prices, default=0.0)

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    # Python Constraints
    @api.constrains("expected_price", "selling_price")
    def _check_selling_price(self):
        for estate in self:
            if not float_is_zero(estate.selling_price, precision_digits=2):
                min_acceptable = estate.expected_price * 0.9
                if (
                    float_compare(
                        estate.selling_price, min_acceptable, precision_digits=2
                    )
                    < 0
                ):
                    raise ValidationError(
                        "Selling price cannot be lower than 90% of the expected price."
                    )

    # Actions
    def action_set_sold(self):
        for estate in self:
            if estate.state == "cancelled":
                raise UserError(_("Cancelled properties cannot be sold."))
            estate.state = "sold"
        return True

    def action_set_cancelled(self):
        for estate in self:
            if estate.state == "sold":
                raise UserError(_("Sold properties cannot be cancelled."))
            estate.state = "cancelled"
        return True
