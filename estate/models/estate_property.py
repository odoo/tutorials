from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo.tools import float_compare, float_is_zero
from datetime import date, timedelta


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate property table'
    _order = 'id desc'

    name = fields.Char(string = 'Title', required = True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(string = 'Available From', copy = False, default = date.today() + timedelta(days=90))
    expected_price = fields.Float(required = True)
    selling_price = fields.Float(readonly = True, copy = False)
    bedrooms = fields.Integer(default = 2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection = [
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')
            ]
        )
    active = fields.Boolean()
    state = fields.Selection(
        selection = [
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled')
            ],
        string = 'Status', required = True, copy = False, default = 'new'
        )
    property_type_id = fields.Many2one('estate.property.type', string = 'Property Type', )
    partner_id = fields.Many2one('res.partner', string = 'Buyer')
    user_id = fields.Many2one('res.users', string = 'Salesman', default = lambda self: self.env.user)
    tag_ids = fields.Many2many('estate.property.tags', string = 'Tags')
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string = 'Offers')
    total_area = fields.Float(compute = '_compute_total')
    best_price = fields.Float(compute = '_compute_best')

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)',
         'The expected price should be strictly positive'),
        ('check_selling_price', 'CHECK(selling_price >= 0)',
         'The expected price should be positive'),
    ]

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for record in self:
            if float_is_zero(record.selling_price, precision_digits=2):
                continue
            if float_compare(record.selling_price, 0.9 * record.expected_price, precision_digits=2) < 0:
                raise UserError('The selling price should be higher than 90%\0 of the expected price')

    @api.depends('living_area', 'garden_area')
    def _compute_total(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area
            

    @api.depends('offer_ids')
    def _compute_best(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped('price'),default = 0)

    @api.onchange('garden')
    def _onchange_garden(self):
        print(self)
        self.garden_area = 10 if self.garden else 0
        self.garden_orientation = 'north' if self.garden else None

    @api.onchange('offer_ids')
    def _onchange_offers(self):
        if self.offer_ids:
            self.state = 'offer_received'
        else:
            self.state = 'new'

    def action_sold(self):
        for record in self:
            if record.state == 'cancelled':
                raise UserError('Cancelled properties cannot be sold')
            record.state = 'sold'

    def action_cancel(self):
        for record in self:
            if record.state == 'sold':
                raise UserError('Sold properties cannot be cancelled')
            record.state = 'cancelled'