from odoo import api, fields, models
from datetime import date, timedelta
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class Estate(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    _order = "id desc"

    name = fields.Char(required=True, default="Unknown")
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    expected_price = fields.Float()
    bedrooms = fields.Integer(default=2)
    last_seen = fields.Datetime("Last Seen", default=fields.Date.today)
    date_availability = fields.Date(default=lambda self: date.today() + timedelta(days=90), copy=False)
    active = fields.Boolean(default=True)
    living_area = fields.Integer(string="Living Area")
    facades = fields.Integer(string="Facades")
    garden = fields.Boolean(string="Garage")
    garden_area = fields.Integer(string="Garden Area")
    garden_orientation = fields.Selection(
        [
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')
        ],
        string="Garden Orientation"
    )
    state = fields.Selection(
    selection=[
        ('new', 'New'),
        ('offer_received', 'Offer Received'),
        ('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('cancelled', 'Cancelled')
        ],
        default='new',
        required=True,
        copy=False
    )
    property_type = fields.Many2one("estate.property.type", string="Property Type")
    buyer = fields.Many2one(
        "res.partner",
        string="Buyer",
        copy=False
    )
    seller = fields.Many2one(
        "res.users",
        string="Salesperson",
        default=lambda self: self.env.user
    )
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many(
    "estate.property.offer", "property_id", string="Offers"
    )
    total_area = fields.Integer(
        string="Total Area",
        compute="_compute_total_area",
        store=True
    )

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    best_price = fields.Float(
        string="Best Offer",
        compute="_compute_best_price"
    )
    selling_price = fields.Float(copy=False)

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            prices = record.offer_ids.mapped("price")
            record.best_price = max(prices) if prices else 0.0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    def action_mark_sold(self):
        for record in self:
            if record.state == 'cancelled':
                raise UserError("Canceled properties cannot be sold.")
            record.state = 'sold'

    def action_mark_cancelled(self):
        for record in self:
            if record.state == 'sold':
                raise UserError("Sold properties cannot be canceled.")
            record.state = 'cancelled'

    _sql_constraints = [
        ('check_expected_price_positive', 'CHECK(expected_price > 0)', 'The expected price must be strictly positive.'),
        ('check_selling_price_positive', 'CHECK(selling_price >= 0)', 'The selling price must be positive.'),
    ]

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price_threshold(self):
        for record in self:
            if float_is_zero(record.selling_price, precision_digits=2):
                continue

            minimum_allowed = record.expected_price * 0.9

            if float_compare(record.selling_price, minimum_allowed, precision_digits=2) < 0:
                raise ValidationError(
                    ("The selling price cannot be lower than 90%% of the expected price.\n"
                    "Expected Price: %.2f, Selling Price: %.2f (Minimum allowed: %.2f)") %
                    (record.expected_price, record.selling_price, minimum_allowed)
                )

    @api.ondelete(at_uninstall=False)
    def _check_property_state_before_delete(self):
        for record in self:
            if record.state not in ['new', 'cancelled']:
                raise UserError("You can only delete properties that are in 'New' or 'Cancelled' state.")
