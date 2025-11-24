# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, exceptions
from odoo.tools.float_utils import float_is_zero, float_compare


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate Property'
    _order = "id desc"

    name = fields.Char('Title', required=True, default='Unknown', translate='True')
    active = fields.Boolean('Active', default=True)
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
            string='Garden orientation',
            selection=[
                ('north', 'North'),
                ('south', 'South'),
                ('east', 'East'),
                ('west', 'West'),
            ],
        )
    state = fields.Selection(
        string='State',
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled'),
        ],
        default='new',
        required=True,
        copy=False,
    )
    property_type_id = fields.Many2one('estate.property.type', string='Property Type')
    property_tag_ids = fields.Many2many('estate.property.tag', string='Property Tag')
    buyer_id = fields.Many2one('res.partner', string='Buyer', copy=False,
                               domain=[('is_company', '=', False)])
    salesperson_id = fields.Many2one('res.users', string='Salesperson',
                                     default=lambda self: self.env.user)
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers')
    total_area = fields.Integer('Total Area (sqm)', compute='_compute_total_area')
    best_offer = fields.Float('Best Offer', compute='_compute_best_offer')

    _check_expected_price = models.Constraint(
        'CHECK(expected_price > 0)',
        'The expected price must be strictly positive',
    )

    _check_selling_price = models.Constraint(
        'CHECK(selling_price >= 0)',
        'The selling price must be positive',
    )

    @api.depends('garden_area', 'living_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends('offer_ids.price')
    def _compute_best_offer(self):
        for record in self:
            record.best_offer = max(record.offer_ids.mapped('price'), default=0.0)

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for record in self:
            if not float_is_zero(record.selling_price, 4) and float_compare(record.selling_price,
                                                                            record.expected_price * 0.9, 4) < 0:
                raise exceptions.ValidationError("The selling price must be at least 90% of the expected price.")

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = ''

    @api.ondelete(at_uninstall=False)
    def _unlink_check_state(self):
        for record in self:
            if record.state not in ('new', 'cancelled'):
                raise exceptions.UserError("Only new and cancelled properties can be deleted.")

    def action_property_sold(self):
        self.ensure_one()
        if self.state != 'cancelled':
            self.state = 'sold'
        else:
            raise exceptions.UserError("Cancelled properties cannot be sold.")
        return True

    def action_property_cancelled(self):
        self.ensure_one()
        if self.state != 'sold':
            self.state = 'cancelled'
        else:
            raise exceptions.UserError("Sold properties cannot be cancelled.")
        return True
