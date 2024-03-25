from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError
from datetime import date
from dateutil.relativedelta import relativedelta
from odoo.tools.float_utils import float_compare


class EsateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Defines a real estate property'
    _order = 'id desc'

    name = fields.Char(string='Title', required=True, index=True)
    description = fields.Text(string='Description')
    postcode = fields.Char(string='Postcode')
    date_availability = fields.Date(string='Available From', copy=False,
                                    default=lambda _: date.today() + relativedelta(months=3))
    expected_price = fields.Float(string='Expected Price', required=True)
    selling_price = fields.Float(string='Selling Price', readonly=True, copy=False)
    bedrooms = fields.Integer(string='Bedrooms', default=2)
    living_area = fields.Integer(string='Living Area (sqm)')
    facades = fields.Integer(string='Facades')
    garage = fields.Boolean(string='Garage')
    garden = fields.Boolean(string='Garden')
    garden_area = fields.Integer(string='Garden Area (sqm)')
    garden_orientation = fields.Selection([
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')
        ],
        'Garden Orientation')
    active = fields.Boolean(string='Active', default=True)
    state = fields.Selection([
        ('new', 'New'),
        ('offer_received', 'Offer Received'),
        ('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('cancelled', 'Cancelled'),
    ], 'State', default='new', required=True)
    property_type_id = fields.Many2one('estate.property.type', string='Property Type')
    buyer_id = fields.Many2one('res.partner', string='Buyer')
    salesperson_id = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.user)
    property_tag_ids = fields.Many2many('estate.property.tag', string='Property Tags')
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers')
    total_area = fields.Integer(string='Total Area (sqm)', compute='_compute_total_area')
    best_offer = fields.Float(string='Best Offer', compute='_compute_best_offer')

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
            record.best_offer = max(self.offer_ids.mapped('price'), default=0.0)

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = None
            self.garden_orientation = None

    @api.onchange('state')
    def _onchange_state(self):
        if self.state in ['offer_accepted', 'sold'] and not self.env['estate.property.offer'].search([('state', '=', 'accepted')]):
            raise UserError('No offer has been accepted!')

        if self.state == 'offer_received' and not self.env['estate.property.offer'].search_count([]):
            raise UserError('No offers have been added!')

        # Reset accepted offer. It might prove useful to retain the accepted offer in case of cancellation as a form of "history".
        if self.state not in ['offer_accepted', 'cancelled']:
            accepted_offer = next(iter(self.env['estate.property.offer'].search([('state', '=', 'accepted')])), None)
            if accepted_offer:
                self.buyer_id = None
                self.selling_price = None
                accepted_offer.state = 'new'

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for record in self:
            if record.selling_price \
                and float_compare(record.selling_price, 0.9 * record.expected_price, precision_digits=2) < 0:
                raise ValidationError('Selling price must be >= 90% of the expected price.')

    @api.ondelete(at_uninstall=False)
    def check_deleted_property(self):
        for record in self:
            if record.state not in ('new', 'cancelled'):
                raise UserError('Cannot delete a propoerty unless it\'s newly created or cancelled!')

    def action_mark_sold(self):
        for record in self:
            if record.state == 'cancelled':
                raise UserError('A cancelled property cannot be sold')

            record.state = 'sold'
            return True

    def action_mark_cancelled(self):
        for record in self:
            if record.state == 'sold':
                raise UserError('A sold property cannot be cancelled')

            record.state = 'cancelled'
            return True

    def _accept_offer(self, offer):
        self.buyer_id = offer.buyer_id
        self.selling_price = offer.price
        self.state = 'offer_accepted'
