from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError
from datetime import date
from dateutil.relativedelta import relativedelta
from odoo.tools.float_utils import float_compare


class EsateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Defines a real estate property'

    name = fields.Char('Title', required=True, index=True)
    description = fields.Text('Description')
    postcode = fields.Char('Postcode')
    date_availability = fields.Date('Available From', copy=False, 
                                    default=lambda _: date.today() + relativedelta(months=3))
    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float('Selling Price', readonly=True, copy=False, compute='_compute_selling_price', store=True)
    bedrooms = fields.Integer('Bedrooms', default=2)
    living_area = fields.Integer('Living Area (sqm)')
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden Area (sqm)')
    garden_orientation = fields.Selection([
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')
        ],
        'Garden Orientation')
    active = fields.Boolean('Active', default=True)
    status = fields.Selection([
        ('new', 'New'),
        ('offer_received', 'Offer Received'),
        ('sold', 'Sold'),
        ('cancelled', 'Cancelled')
    ], 'Status', default='new')

    property_type_id = fields.Many2one('estate.property.type', string='Property Type')

    buyer_id = fields.Many2one('res.partner', string='Buyer')
    salesperson_id = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.user)

    property_tag_ids = fields.Many2many('estate.property.tag', string='Property Tags')

    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers')

    total_area = fields.Integer('Total Area (sqm)', compute='_compute_total_area')

    best_offer = fields.Float('Best Offer', compute='_compute_best_offer')

    accepted_offer_id = fields.Many2one('estate.property.offer', string='Accepted Offer')

    _sql_constraints = [
        ('check_expected_price', 
         'CHECK(expected_price > 0)', 
         'Expected price must be strictly positive.'),
    ]

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_offer(self):
        for record in self: 
            record.best_offer = max(self.offer_ids.mapped('price'), default=0.)

    @api.depends('accepted_offer_id')
    def _compute_selling_price(self):
        for record in self:
            record.selling_price = record.accepted_offer_id.price if record.accepted_offer_id else None

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = None
            self.garden_orientation = None

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for record in self:
            if record.selling_price \
                and float_compare(record.selling_price, 0.9 * record.expected_price, precision_digits=2) < 0:
                raise ValidationError('Selling price must be >= 90% of the expected price.')

    def action_mark_sold(self):
        for record in self:
            if record.status == 'cancelled':
                raise UserError('A cancelled property cannot be sold')

            record.status = 'sold'
            return True

    def action_mark_cancelled(self):
        for record in self:
            if record.status == 'sold':
                raise UserError('A sold property cannot be cancelled')

            record.status = 'cancelled'
            return True
        
    def _accept_offer(self, offer):
        self.accepted_offer_id = offer
        self.buyer_id = offer.buyer_id
