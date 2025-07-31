from datetime import date, timedelta

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare, float_is_zero


class NinjaTurtlesEstate(models.Model):
    _name = "ninja.turtles.estate"
    _description = "For the fastest progress ever!"
    _order = "id desc"
    _inherit = ['mail.thread']

    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(
        string="Available From",
        copy=False,
        default=lambda self: date.today() + timedelta(days=90),
    )
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(
        string="Selling Price",
        readonly=True,
        copy=False,
    )
    bedrooms = fields.Integer(
        string="Bedrooms",
        default=2,
    )
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West'),
        ],
        help="Garden Orientation is for choosing your specified area for your garden.",
    )
    status = fields.Selection(
        string="Status",
        selection=[
            ('new', 'New'),
            ('offer received', 'Offer Received'),
            ('offer accepted', 'Offer Accepted'),
            ('sold', "Sold"),
            ('cancelled', "Cancelled"),
        ],
        required=True,
        default="new",
        copy=False,
        tracking=True,
    )
    active = fields.Boolean(
        string="Active",
        default=True,
    )
    total_area = fields.Integer(
        string="Total Area",
        compute="_compute_total_area",
    )
    best_price = fields.Float(
        string="Best Offer",
        compute="_compute_best_price",
    )
    property_type_id = fields.Many2one(
        "ninja.turtles.estate.property.type",
        string="Property Type",
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
    tag_ids = fields.Many2many(
        "ninja.turtles.estate.property.tag",
        string="Tags",
    )
    offer_ids = fields.One2many(
        "ninja.turtles.estate.property.offer",
        "property_id",
        string="Offers",
        tracking=True,
    )

    _sql_constraints = [
        ('check_expected_price_positive', 'CHECK(expected_price > 0)', 'Expected price must be strictly positive.'),
        ('check_selling_price_positive', 'CHECK(selling_price >= 0)', 'Selling price must be positive.'),
    ]

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            prices = record.offer_ids.mapped("price")
            record.best_price = max(prices) if prices else 0.0

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False

    def action_mark_sold(self):
        for record in self:
            if record.status in ('cancelled', 'new'):
                raise UserError("Cancelled or new properties cannot be sold.")
            elif record.status == 'offer received':
                raise UserError("You cannot sell a property with a non-accepted offer.")
            else:
                record.status = 'sold'
        return True

    def action_cancel(self):
        for record in self:
            if record.status == 'sold':
                raise UserError("Sold properties cannot be cancelled.")
            record.status = 'cancelled'
        return True

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price_margin(self):
        for record in self:
            if float_is_zero(record.selling_price, precision_digits=2):
                continue  # allow 0 (no offer accepted yet)
            min_price = 0.9 * record.expected_price
            if float_compare(record.selling_price, min_price, precision_digits=2) < 0:
                raise ValidationError(
                    "Selling price cannot be lower than 90% of the expected price.\n"
                    f"Expected: {record.expected_price}, Minimum Allowed: {min_price}, Given: {record.selling_price}"
                )

    @api.ondelete(at_uninstall=False)
    def _check_property_deletion(self):
        for record in self:
            if record.status not in ['new', 'cancelled']:
                raise UserError("You can only delete properties in 'New' or 'Cancelled' status.")
