from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"
    _order = "id desc"

    name = fields.Char(
        string="Property Title",
        required=True,
        help="Enter the Name of the property",
        index="trigram",
    )
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(
        index="btree",
        string="Available From",
        copy=False,
        default=lambda self: fields.Date.today() + relativedelta(months=3),
    )
    expected_price = fields.Float(required=True, string="Expected Price")
    selling_price = fields.Float(readonly=True, copy=False, string="Selling Price")
    bedrooms = fields.Integer(default=2, string="Bedrooms")
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        [
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West")
        ],
        string="Garden Orientation"
    )
    active = fields.Boolean(default=True, string="Active")
    state = fields.Selection(
        [
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        string="State",
        required=True,
        copy=False,
        default="new"
    )
    property_type_ids = fields.Many2one(
        comodel_name="estate.property.type",
        string="Property Type",
    )
    tag_ids = fields.Many2many(
        comodel_name="estate.property.tag",
        string="Property Tag",
        relation="estate_property_tag_rel",
        column1='estate_property_ids',
        column2="estate_property_tag_ids"
    )
    salesperson_ids = fields.Many2one(
        'res.users',
        string="Salesperson",
        default=lambda self: self.env.user
    )
    buyer_ids = fields.Many2one(
        'res.partner',
        string="Buyer"
    )
    offer_ids = fields.One2many(
        "estate.property.offer",
        "property_ids",
        string="Property Offers"
    )
    total_area = fields.Float(compute="_compute_total_area", string="Total Area (sqm)")
    best_price = fields.Float(compute="_compute_best_price", string="Best Price")
    validity = fields.Integer(string="Validity (days)", default=7)

    _check_expected_price = models.Constraint(
        'CHECK(expected_price > 0)',
        'Expected Price can be strictly positive'
    )
    _check_selling_price_positive = models.Constraint(
        'CHECK(selling_price >= 0)',
        'Selling price can be strictly positive'
    )

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            prices = record.offer_ids.mapped("price")
            record.best_price = max(prices, default=0.0)

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    def action_to_sold(self):
        for record in self:
            if record.state == "cancelled":
                raise UserError("A cancelled property cannot be sold")
            record.state = "sold"
        return True

    def action_to_cancel(self):
        for record in self:
            if record.state == "sold":
                raise UserError("A sold property cannot be cancelled")
            record.state = "cancelled"
        return True

    @api.constrains("expected_price", "selling_price")
    def _check_selling_price(self):
        for record in self:
            if float_is_zero(record.selling_price, precision_digits=2):
                continue

            minimum_price = record.expected_price * 0.9
            result = float_compare(
                record.selling_price,
                minimum_price,
                precision_digits=2
            )
            if result == -1:
                raise ValidationError(
                    "The Selling Price should 90% of the Expected Price"
                )
