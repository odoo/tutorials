# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import timedelta
from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError


class EstateProperty(models.Model):
    _name = 'estate.property'
    _inherit = ['rating.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = 'Estate Property model'
    _order = 'id desc'

    name = fields.Char(string='Title', required=True, tracking=True)
    description = fields.Text(string='Description')
    postcode = fields.Char(string='Postcode')
    date_availability = fields.Date(string='Available From', copy=False, default=fields.Date.today() + timedelta(days=90))
    expected_price = fields.Monetary(string='Expected Price', default=2, required=True, currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)
    selling_price = fields.Monetary(string='Selling Price', readonly=True, currency_field='currency_id')
    bedrooms = fields.Integer(string='Bedrooms')
    living_area = fields.Integer(string='Living Area (sqm)')
    facades = fields.Integer(string='Facades')
    garage = fields.Boolean(string='Garage')
    garden = fields.Boolean(string='Garden')
    garden_area = fields.Integer(string='Garden Area')
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West')
    ], string='Garden Orientation')
    active = fields.Boolean(default=True)
    state = fields.Selection([
        ('new', 'New'),
        ('offer_received', 'Offer Received'),
        ('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('cancelled', 'Cancelled')
    ], string='Status', required=True, copy=False, default='new', tracking=True)
    property_type_id = fields.Many2one('estate.property.type', string='Property Type')
    salesperson_id = fields.Many2one('res.users', string='Salesman', tracking=True)
    buyer_id = fields.Many2one('res.partner', string='Buyer', copy=False, tracking=True)
    tag_ids = fields.Many2many('estate.property.tag', string='Property Tag')
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offer')
    total_area = fields.Float(compute='_compute_total_area', string='Total Area (sqm)')
    best_price = fields.Monetary(compute='_compute_best_price', string='Best Offer', currency_field='currency_id')
    estate_property_sequence = fields.Char(string='Reference', readonly=True, copy=False)
    company_id = fields.Many2one('res.company', required=True, string='Company', default=lambda self: self.env.company)

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0.0)', 'The expected price must be strictly positive.'),
        ('check_selling_price', 'CHECK(selling_price > 0.0)', 'The selling price must be strictly positive.')
    ]

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped('price'), default=0)

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        if self.selling_price and self.selling_price < 0.9 * self.expected_price:
            raise ValidationError(_("Selling price must be atleast 90% of expected price"))

    @api.ondelete(at_uninstall=False)
    def _unlink_except_new_or_cancel(self):
        for record in self.filtered(lambda record: record.state not in ['new', 'cancelled']):
            raise UserError(_("In order to delete a property, it must be new or cancelled."))

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('estate_property_sequence'):
                vals['estate_property_sequence'] = self.env['ir.sequence'].next_by_code('estate.property.sequence')
        return super().create(vals_list)

    def action_cancel(self):
        for record in self:
            if record.state == 'sold':
                raise UserError(_("Sold properties cannot be cancelled."))
            else:
                record.state = 'cancelled'
        return True

    def action_sold(self):
        for record in self:
            if record.state == 'cancelled':
                raise UserError(_("Cancelled properties cannot be sold."))
            if record.state != 'offer_accepted':
                raise UserError(_("Offer cannot be sold without offer accepted."))
            else:
                record.state = 'sold'
        template = self.env.ref('estate.estate_rating_template')
        for record in self:
            if record.buyer_id:
                template.send_mail(record.id, force_send=True)
        return True

    def rating_get_partner_id(self):
        """Defines which partner is providing the rating (e.g., the customer)"""
        return self.buyer_id

    def rating_get_rated_partner_id(self):
        """Defines which partner is being rated (e.g., the responsible user)"""
        return self.salesperson_id.buyer_id

    def _track_subtype(self, init_values):
        self.ensure_one()
        if 'state' in init_values and self.state == 'offer_accepted':
            return self.env.ref('estate.mt_state_change')
        return super()._track_subtype(init_values)
