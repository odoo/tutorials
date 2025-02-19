# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api,fields, models
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError
from odoo.tools.float_utils import float_compare

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    _order = "id desc"
    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)', 'Property expected price must be strictly positive!'),
        ('check_selling_price', 'CHECK(selling_price >= 0)', 'Property selling price must be positive!'),
    ]

    name = fields.Char(string='Title', required=True)
    company_id = fields.Many2one('res.company', required=True, default=lambda self: self.env.company)
    description = fields.Text(string='Description', translate=True)
    postcode = fields.Char(string='Postcode')
    date_availability = fields.Date(string='Available From', copy=False, default=lambda self: fields.Date.add(fields.Date.today(), months=3))
    expected_price = fields.Float(string='Expected Price', required=True)
    selling_price = fields.Float(string='Selling Price', readonly=True, copy=False)
    bedrooms = fields.Integer(string='Bedrooms', default=2)
    living_area = fields.Integer(string='Living Area (sqm)')
    facades = fields.Integer(string='Facades')
    garage = fields.Boolean(string='Garage')
    garden = fields.Boolean(string='Garden')
    garden_area = fields.Integer(string='Garden Area (sqm)')
    garden_orientation = fields.Selection(
        selection=[
            ('north','North'),
            ('south','South'),
            ('east','East'),
            ('west','West')
        ],
        string='Garden Orientation'
    )
    active = fields.Boolean(string='Active', default=True)
    state = fields.Selection(string='Status',
        selection=[
            ('new','New'),
            ('offer_received','Offer Received'),
            ('offer_accepted','Offer Accepted'),
            ('sold','Sold'),
            ('cancelled','Cancelled')
        ],
        default='new', required=True, copy=False
    )
    property_type_id = fields.Many2one('estate.property.type')
    partner_id = fields.Many2one('res.partner', string='Buyer', copy=False)
    user_id = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.user)
    tag_ids = fields.Many2many('estate.property.tag', string='Tags')
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers')
    total_area =  fields.Integer(string='Total Area (sqm)', compute='_compute_total_area')
    best_price = fields.Float(string='Best Offer', compute='_compute_best_price')
    image = fields.Binary(string='Image')

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            prices = record.offer_ids.mapped('price')
            record.best_price = max(prices) if prices else 0

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = ''

    def action_sold(self):
        for record in self:
            if record.state == 'cancelled':
                raise UserError("Cancelled properties cannot be sold.")
            else:
                record.state = 'sold'
        return True

    def action_cancel(self):
        for record in self:
            if record.state == 'sold':
                raise UserError("Sold properties cannot be cancelled.")
            else:
                record.state = 'cancelled'
        return True

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for record in self:
            if record.selling_price != 0:
                difference_in_price = float_compare(record.selling_price, record.expected_price*90/100, precision_digits=0)
                if difference_in_price < 0:
                    raise ValidationError(r"Selling price cannot be less than 90% of the expected price.")

    @api.ondelete(at_uninstall=False)
    def _unlink_check(self):
        for record in self:
            if record.state not in ['new', 'cancelled']:
                raise UserError("Only new and cancelled properties can be deleted.")
