# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _
from datetime import timedelta
from odoo.exceptions import UserError, ValidationError

class Property(models.Model):
    _name = "estate.property"
    _description = "Estate property details"
    _order = "id desc"

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    
    postcode = fields.Char(string='Postal code')
    
    date_availability = fields.Date(string='Availability Date', copy=False,
                                    default=fields.Date.today()+timedelta(days=90))

    expected_price = fields.Float(string='Expected Price', required=True, default=1.0)
    selling_price = fields.Float(string='Selling Price', readonly=True, copy=False)
    best_price = fields.Float(string='Best Offer', readonly=True, copy=False,
                              compute="_compute_best_offer")
    
    bedrooms = fields.Integer(string='Number of bedrooms', default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([('north', 'North'), ('south', 'South'),
                                            ('east', 'East'), ('west', 'West')])

    active = fields.Boolean(default=True)
    
    state = fields.Selection([('new', 'New'), ('offer received', 'Offer Received'),
                              ('offer accepted', 'Offer Accepted'), ('cancelled', 'Cancelled'),
                              ('sold', 'Sold')],
                               default="new",
                               required=True,
                               copy=False)

    total_area = fields.Integer(string='Total Area (sqm)', compute="_compute_total_area",
                                readonly=True, copy=False)

    _sql_constraints = [
        ('check_epxected_price', 'CHECK(expected_price > 0)', 'The expected price should be greater than 0.'),
        ('check_selling_price', 'CHECK(selling_price >= 0)', 'The selling price should be greater than or equal to 0.')
    ]
    
    property_type_id = fields.Many2one(
        'estate.property.type',
        string="Type",
        help="Select the category for this product"
    )

    property_seller_id = fields.Many2one(
        'res.users',
        string='Salesperson',
        default=lambda self: self.env.user
    ) 

    property_buyer_id = fields.Many2one(
        'res.partner',
        string='Buyer',
        copy=False
    )

    property_tag_ids = fields.Many2many(
        'estate.property.tag',
        copy=False
    )

    offer_ids = fields.One2many(
        comodel_name='estate.property.offer',
        inverse_name='property_id',
        string="Offers",
        copy=False
    )

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area 

    @api.depends("offer_ids.price")
    def _compute_best_offer(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped('price')) if record.offer_ids else 0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = ''
    
    @api.constrains('expected_price')
    def _check_expected_price(self):
        for record in self:
            if record.expected_price <= 0:
                raise ValidationError('The expected price must be greater than zero.')

    @api.constrains('selling_price')
    def _check_selling_price(self):
        for record in self:
            if record.selling_price < 0:
                raise ValidationError('The selling price should be positive.')

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price_expected(self):
        for record in self:
            if record.selling_price < record.expected_price * 0.9 and (not (record.selling_price == 0)) :
                raise ValidationError('The selling price should never be lower than 90 percent of the expected price.')

    def action_cancel_the_property(self):
        for record in self:
            if record.state == 'sold':
                raise UserError(_('Sold properties cannot be cancelled.'))
            record.state = 'cancelled'
        return True

    def action_sell_the_property(self):
        for record in self:
            if record.state == 'cancelled':
                raise UserError(_('Cancelled properties cannot be sold.'))
            else:
                record.state = 'sold'
        return True
