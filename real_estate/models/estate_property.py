from datetime import date, timedelta
from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"
    _order = "id desc"

    name = fields.Char(default="Unknown", required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    availability_date = fields.Date(default=lambda self: date.today() + timedelta(days=90), copy=False)
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    _sql_constraints = [
    ('check_expected_price_positive', 'CHECK(expected_price > 0)', 'The expected price must be strictly positive.'),
    ('check_selling_price_positive', 'CHECK(selling_price >= 0)', 'The selling price must be positive.')
]
    bedrooms = fields.Integer(default=2)
    living_area = fields.Float(string="Living Area")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Float(string="Garden Area")
    total_area = fields.Float(string="Total Area", compute="_compute_total_area")
    garden_orientation = fields.Selection(
        [
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')
        ],
        string="Garden Orientation"
    )
    active = fields.Boolean(default=False)
    state = fields.Selection(
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled'),
        ],
        required=True,
        copy=False,
        default='new'
    )
    property_type_id = fields.Many2one('estate.property.type', string="Property Type")
    buyer_id = fields.Many2one('res.partner', string="Buyer", copy=False)
    salesperson_id = fields.Many2one('res.users', string="Salesperson", default=lambda self: self.env.user)
    tag_ids = fields.Many2many('estate.property.tag', string="Tags")
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string="Offers")
    best_price = fields.Float(string="Best Offer", compute="_compute_best_price")
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company
    )

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for record in self:
            if (float_is_zero(record.selling_price, precision_digits=2)
            or record.state not in ['offer_accepted', 'sold']):
                continue
            min_acceptable_price = 0.9 * record.expected_price
            if float_compare(record.selling_price, min_acceptable_price, precision_digits=2) < 0:
                raise ValidationError("Selling price cannot be lower than 90% of the expected price.")

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = (record.living_area or 0.0) + (record.garden_area or 0.0)

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            prices = record.offer_ids.mapped('price')
            record.best_price = max(prices) if prices else 0.0

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False

    def action_cancel(self):
        for record in self:
            if record.state == 'sold':
                raise UserError("Sold properties cannot be cancelled.")
            record.state = 'cancelled'
        return True

    def action_sold(self):
        for record in self:
            if record.state == 'cancelled':
                raise UserError("Cancelled properties cannot be sold.")
            record.state = 'sold'
        return True

    @api.ondelete(at_uninstall=False)
    def _check_deletion(self):
        for record in self:
            if record.state not in ['new', 'cancelled']:
                raise UserError("You can only delete a property if its state is 'New' or 'Cancelled'.")
