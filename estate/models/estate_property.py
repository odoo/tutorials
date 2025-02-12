# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from datetime import timedelta
from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class Estateproperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate property'

    name = fields.Char(string='Property Name',
                       required=True, default='Property')
    property_type_id = fields.Many2one(
        'estate.property.type', string='Property Type')
    salesperson_id = fields.Many2one(
        'res.users', string='Salesperson', default=lambda self: self.env.user)
    buyer_id = fields.Many2one(
        'res.partner', string='Buyer', copy=False)
    tag_ids = fields.Many2many('estate.property.tag', string='Tags')
    offer_ids = fields.One2many(
        'estate.property.offer', 'property_id', string='Offers')
    description = fields.Text(string='Description', compute='_compute_desc')
    bedrooms = fields.Integer(string='Bedrooms', default=2)
    living_area = fields.Integer(string='Living Area')
    facades = fields.Integer(string='Facades')
    garage = fields.Boolean(string='Garage')
    garden = fields.Boolean(string='Garden')
    garden_area = fields.Integer(string='Garden Area')
    garden_orientation = fields.Selection(
        string='Type',
        selection=[('north', 'North'), ('south', 'South'),
                   ('east', 'East'), ('west', 'West')]
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        string='State',
        selection=[('new', 'New'), ('offered_rec', 'Offer recieved'), ('offer_acc',
                                                                       'Offer Accepted'), ('sold', 'Sold'), ('cancel', 'Cancelled')],
        required=True,
        copy=False,
        default='new'
    )
    total_area = fields.Integer(
        string='Total Area', compute='_compute_total_area')
    best_price = fields.Float(
        string='Best Price', compute='_compute_best_price')
    offer_recieved = fields.Boolean(
        compute='_compute_offer_recieved', store=True)

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)',
         'The expected price must be strictly positive.'),
        ('check_selling_price', 'CHECK(selling_price >= 0)',
         'The selling price must be positive.'),
    ]

    @api.constrains('selling_price')
    def _check_selling_price(self):
        for record in self:
            if record.selling_price < 0:
                raise ValidationError('The selling price must be positive.')

    @api.constrains('expected_price')
    def _check_expected_price(self):
        for record in self:
            if record.expected_price < 0:
                raise ValidationError('The expected price must be positive.')

    @api.constrains('expected_price', 'selling_price')
    def _check_selling_price(self):
        for record in self:
            if not float_is_zero(record.selling_price, precision_digits=2):
                min_acceptable_price = record.expected_price * 0.9
                if float_compare(record.selling_price, min_acceptable_price, precision_digits=2) == -1:
                    raise ValidationError(
                        'The selling price cannot be lower than 90% of the expected price.')

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for property in self:
            prices = property.offer_ids.mapped('price')
            property.best_price = max(prices, default=0)

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False

    def action_cancel(self):
        for property in self:
            if property.state == 'sold':
                raise UserError('A sold property cannot be cancelled.')
            else:
                property.state = 'cancel'

    def action_sold(self):
        for property in self:
            if property.state == 'cancel':
                raise UserError('A cancelled property cannot be sold.')
            if not property.offer_ids:
                raise UserError('Cannot sold without any offer.')
            else:
                property.state = 'sold'

    @api.depends('offer_ids')
    def _compute_offer_recieved(self):
        for record in self:
            record.offer_recieved = bool(record.offer_ids)

    @api.depends('salesperson_id.name')
    def _compute_desc(self):
        for record in self:
            record.description = 'Test for salesperson %s' % record.salesperson_id.name
    postcode = fields.Char('PostCode')
    date_availability = fields.Date(
        'Available From', copy=False, default=lambda self: fields.Datetime.today() + timedelta(days=90))
    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float('Selling Price', readonly=True, copy=False)

    @api.ondelete(at_uninstall=False)
    def _unlink_if_property_in_cancel_or_new_state(self):
        for record in self:
            if record.state not in ('new', 'cancel'):
                raise UserError(
                    'You can only delete properties that are in new or cancel state.')
 