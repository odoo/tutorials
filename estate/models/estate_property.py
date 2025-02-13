from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero

class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate Property'
    _order = 'id desc'

    name = fields.Char(string='Title', required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(string='Available From', copy=False, default=fields.Date.today()+ relativedelta(months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string='Living Area (sqm)')
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string='Garden Area (sqm)')
    garden_orientation = fields.Selection(
        selection=[
            ('north','North'),
            ('south','South'),
            ('east','East'),
            ('west','West'),
        ]
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        required=True,
        default='new',
        copy=False,
        selection=[
            ('new','New'),
            ('offer_received','Offer Received'),
            ('offer_accepted','Offer Accepted'),
            ('sold','Sold'),
            ('cancelled','Cancelled'),
        ],
    )
    property_type_id = fields.Many2one('estate.property.type', string='Property Type')
    user_id = fields.Many2one('res.users', string='Salesman', default=lambda self: self.env.user)
    partner_id = fields.Many2one('res.partner', string='Buyer', copy=False)
    tag_ids = fields.Many2many('estate.property.tag', string='Tags')
    offer_ids = fields.One2many('estate.property.offer', inverse_name='property_id', string='Offers')
    total_area = fields.Integer(string='Total Area (sqm)', compute='_compute_total_area')
    best_price = fields.Float(string='Best Offer', compute='_compute_best_offer')

    @api.depends('living_area','garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area+record.garden_area
    
    @api.depends('offer_ids.price')
    def _compute_best_offer(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped('price'))
            else:
                record.best_price = 0

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden == True:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False

    @api.constrains('selling_price','expected_price')
    def check_selling_price(self):
        for record in self:
            if not float_is_zero(record.selling_price, precision_digits=1) and float_compare(record.selling_price, 0.9 * record.expected_price, precision_digits=1) == -1:
                raise ValidationError(_('The selling price must be at least 90% of the expected price! You must reduce expected price if you want to accept this offer'))

    def action_sold_property(self):
        for record in self:
            if record.state == 'cancelled':
                raise UserError(_('Cancelled properties cannot be sold'))
            record.state = 'sold'
        return True

    def action_cancel_property(self):
        for record in self:
            if record.state == 'sold':
                raise UserError(_('Sold properties cannot be cancel'))
            record.state = 'cancelled'
        return True
    
    _sql_constraints = [
        ('check_expected_price','CHECK(expected_price > 0)','The expected price must be strictly positive'),
        ('check_selling_price','CHECK(selling_price >= 0)','The selling price must be positive'),
    ]
