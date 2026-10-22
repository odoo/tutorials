# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, exceptions, fields, models
from odoo.tools import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = "Real Estate Property"
    _explanation = "Defines a real estate property"
    _order = "name"

    name = fields.Char('Title', required=True)
    description = fields.Text('Description')
    postcode = fields.Char('Postcode')
    date_availability = fields.Date('Available From', copy=False, default=fields.Date.add(fields.Date.today(), months=3))
    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float('Selling Price', readonly=True, copy=False)
    bedrooms = fields.Integer('Bedrooms', default=2)
    living_area = fields.Integer('Living Area (sqm)')
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden Area (sqm)')
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        help="Main orientation of the garden")
    state = fields.Selection(
        string='Status',
        selection=[('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'), ('cancelled', 'Cancelled')],
        required=True,
        copy=False,
        default='new',
        help="Status of the property")
    active = fields.Boolean('Active', default=True)
    property_type_id = fields.Many2one('estate.property.type', string='Property Type')
    buyer_id = fields.Many2one('res.partner', string='Buyer', copy=False)
    seller_id = fields.Many2one('res.users', string='Salesman', default=lambda self: self.env.user)
    property_tag_ids = fields.Many2many('estate.property.tag', string='Tags')
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers')
    total_area = fields.Integer('Total Area (sqm)', compute='_compute_total_area')
    best_price = fields.Float('Best Price', compute='_compute_best_price')

    _check_prices = models.Constraint(
        'CHECK(expected_price > 0.0 AND selling_price > 0.0)',
        'The expected and selling prices must be strictly positive.',
    )

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped('price'), default=0.0)

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = None

    def action_property_sold(self):
        for record in self:
            if record.state == 'cancelled':
                raise exceptions.UserError("Cancelled properties cannot be sold.")
            record.state = 'sold'

    def action_property_cancel(self):
        for record in self:
            if record.state == 'sold':
                raise exceptions.UserError("Sold properties cannot be cancelled.")
            record.state = 'cancelled'

    @api.constrains('expected_price', 'selling_price')
    def _check_selling_price(self):
        for record in self:
            if (not float_is_zero(record.selling_price, precision_digits=0)
                and float_compare(record.selling_price, record.expected_price * 0.9, precision_digits=2) < 0):
                raise exceptions.ValidationError("The selling price cannot be lower than 90% of the expected price")
