# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, exceptions, fields, models
from odoo.tools.float_utils import float_compare


class Property(models.Model):
    _name = 'estate.property'
    _description = 'Estate properties model'
    _order = 'id desc'

    name = fields.Char('Title', required=True)
    description = fields.Text()
    postcode = fields.Char()
    property_type_id = fields.Many2one('estate.property.type')
    tag_ids = fields.Many2many('estate.property.tag')

    date_availability = fields.Date('Available From')
    expected_price = fields.Float(required=True, default=100)
    best_offer = fields.Float(compute='_compute_best_offer')
    selling_price = fields.Float(default=0.0, readonly=True)

    bedrooms = fields.Integer()
    living_area = fields.Integer('Living Area (m²)')
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer('Garden Area (m²)')
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[
            ('north', 'North'),
            ('east', 'East'),
            ('south', 'South'),
            ('west', 'West')
        ]
    )
    total_area = fields.Integer(
        'Total Area (m²)', compute='_compute_total_area')

    active = fields.Boolean(default=True)
    state = fields.Selection(string='Status', required=True, default='new', readonly=True, selection=[
        ('new', 'New'),
        ('offer_received', 'Offer received'),
        ('offer_accepted', 'Offer accepted'),
        ('sold', 'Sold'),
        ('cancelled', 'Cancelled')
    ])
    buyer_id = fields.Many2one('res.partner', readonly=True)
    user_id = fields.Many2one(
        'res.users', string='Salesperson', default=lambda self: self.env.user)
    offer_ids = fields.One2many(
        'estate.property.offer', 'property_id', string='Offers')

    _sql_constraints = [
        ('selling_price_positive', 'check (selling_price >= 0.0)',
         'The selling price must be strictly positive!'),
        ('expected_price_positive', 'check (expected_price > 0)',
         'The expected price must be strictly positive!'),
    ]

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = None

    @api.depends('offer_ids.price')
    def _compute_best_offer(self):
        for record in self:
            record.best_offer = max(record.mapped(
                'offer_ids.price'), default=0.0)

    @api.onchange('offer_ids')
    def _onchange_offer_ids(self):
        for record in self:
            if record.state == 'new' and len(record.offer_ids) > 0:
                record.state = 'offer_received'

    @api.constrains('expected_price', 'selling_price')
    def _check_price(self):
        for record in self:
            if record.state != 'sold' and record.selling_price == 0:
                continue
            if float_compare(record.selling_price, record.expected_price * 0.9, precision_digits=2) < 0:
                raise exceptions.ValidationError(
                    'The selling price must be at least 90% of the expected price')

    @api.ondelete(at_uninstall=False)
    def _unlink_if_new_or_cancelled(self):
        if any(not rec.state in ('new', 'cancelled') for rec in self):
            raise exceptions.UserError(
                'Only new or cancelled properties can be deleted')

    def action_cancel(self):
        for record in self:
            if record.state == 'sold':
                raise exceptions.UserError(
                    'Sold properties can not be cancelled')
            record.state = 'cancelled'
        return True

    def action_sold(self):
        for record in self:
            match record.state:
                case 'cancelled':
                    raise exceptions.UserError(
                        'Cancelled properties can not be sold')
                case 'offer_accepted':
                    record.state = 'sold'
                    return True
                case _:
                    raise exceptions.UserError(
                        'Properties must have an accepted offer in order to be sold')
