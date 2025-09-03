# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import datetime, timedelta
from odoo import api, models, fields
from odoo.exceptions import UserError, ValidationError


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate Property'
    _order = 'id desc'

    name = fields.Char(string='Estate Property Name', required=True)
    description = fields.Text(string='Estate Property Description')
    postcode = fields.Char(string='Estate Property Postcode')
    date_availability = fields.Date(string='Estate Property Date Availability', copy=False, default=lambda self: datetime.now() + timedelta(days=90))
    expected_price = fields.Float(string='Expected Price Of Property', required=True)
    selling_price = fields.Float(string='Selling Price of Property', readonly=True, copy=False)
    bedrooms = fields.Integer(string='Number of Bedrooms in Property', default=2)
    living_area = fields.Integer(string='Number of Living Room in Property')
    facades = fields.Integer(string='Number of Facades in Property')
    garage = fields.Boolean(string='Property have garage or not')
    garden = fields.Boolean(string='Property have Garden or not')
    garden_area = fields.Integer(string='Number of Garden Area')
    garden_orientation = fields.Selection(
        string='Orientation of Garden',
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')
        ],
        help='Different Types of Directions')
    active = fields.Boolean(default=True)
    state = fields.Selection(
        string='State',
        default='new',
        copy=False,
        required=True,
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancel', 'Cancelled')
        ],
        help='State of the property')
    property_type_id = fields.Many2one('estate.property.type', string='Property Type Id')
    buyer_id = fields.Many2one('res.partner', string='Buyer', copy=False)
    salesman_id = fields.Many2one('res.users', string='Salesman', default=lambda self: self.env.user)
    tag_ids = fields.Many2many('estate.property.tag', string='Tags')
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='offer')
    total_area = fields.Float(compute='_compute_total_area')
    best_price = fields.Float(compute='_compute_best_price', string='Best Offer Price')

    _sql_constraints = [
        ('expected_price', 'CHECK(expected_price > 0)', 'Expected price of the property must be positive'),
        ('selling_price', 'CHECK(selling_price >= 0)', 'Selling price of the property must be positive'),
    ]

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped('price'), default=0.0)

    @api.onchange('garden')
    def _onchange_garden(self):
        for record in self:
            if record.garden:
                record.garden_area = 10
                record.garden_orientation = 'north'
            else:
                record.garden_area = False
                record.garden_orientation = False

    def property_sold_action(self):
        for record in self:
            if record.state == 'cancel':
                raise UserError('Cancelled property can not be sold')
            else:
                record.state = 'sold'
        return True

    def property_cancel_action(self):
        for record in self:
            if record.state == 'sold':
                raise UserError('Sold property can not be cancelled')
            else:
                record.state = 'cancel'
        return True

    @api.constrains('selling_price')
    def check_offer_price(self):
        for record in self:
            if record.offer_ids.price < (0.9 * record.expected_price):
                raise ValidationError(f'Selling price ({record.selling_price}) should be greater than 90% ({round(0.9 * record.expected_price, 2)}) of the expected price ({record.expected_price})')

    @api.ondelete(at_uninstall=False)
    def _unlink_if_user_state(self):
        if any(user.state not in ['new', 'cancel'] for user in self):
            raise UserError('Can\'t delete property which is in offer received or offer accepted or sold state.')
