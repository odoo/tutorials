# -*- coding: utf-8 -*-
from dateutil.relativedelta import relativedelta
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError

class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Real Estate Property Information'
    _order = 'name asc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    def _get_default_currency_id(self):
        return self.env.company.currency_id.id

    name = fields.Char(string='Title', required=True, index=True, tracking=True)
    description = fields.Text(string='Full Description')
    notes = fields.Html(string='Internal Notes')
    postcode = fields.Char(string='Postcode / ZIP Code')
    date_availability = fields.Date(
        string='Available From', copy=False,
        default=lambda self: fields.Date.today() + relativedelta(months=+3),
        tracking=True
    )
    expected_price = fields.Float(
        string='Expected Price', required=True,
        digits='Property Price', tracking=True
    )
    selling_price = fields.Float(
        string='Selling Price', readonly=True, copy=False,
        digits='Property Price', tracking=True
    )
    bedrooms = fields.Integer(string='Bedrooms', default=2, tracking=True)
    living_area = fields.Integer(string='Living Area (sqm)', tracking=True)
    facades = fields.Integer(string='Number of Facades')
    garage = fields.Boolean(string='Has Garage?', default=False)
    garden = fields.Boolean(string='Has Garden?', default=False)
    garden_area = fields.Integer(string='Garden Area (sqm)') # tracking=True removed
    garden_orientation = fields.Selection(
        selection=[
            ('N', 'North'), ('S', 'South'), ('E', 'East'), ('W', 'West'),
            ('NE', 'North-East'), ('NW', 'North-West'), ('SE', 'South-East'), ('SW', 'South-West'),
        ],
        string='Garden Orientation'
    )
    active = fields.Boolean(string='Active', default=True)
    state = fields.Selection(
        selection=[
            ('new', 'New'), ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'), ('canceled', 'Canceled')
        ],
        string='Status', required=True, copy=False, default='new', index=True, tracking=True
    )
    currency_id = fields.Many2one(
        'res.currency', string='Currency', required=True,
        default=_get_default_currency_id
    )
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company, required=True, readonly=True) # Explicit company_id
    property_type_id = fields.Many2one('estate.property.type', string='Property Type', tracking=True)
    user_id = fields.Many2one(
        'res.users', string='Salesperson',
        default=lambda self: self.env.user, tracking=True
    )
    buyer_id = fields.Many2one('res.partner', string='Buyer', copy=False, tracking=True)
    tag_ids = fields.Many2many('estate.property.tag', string='Tags')
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers')

    total_area = fields.Integer(
        string="Total Area (sqm)", compute='_compute_total_area', store=True,
        help="Total area: Living Area + Garden Area"
    )
    best_offer = fields.Float(string="Best Offer", compute='_compute_best_offer', help="Highest offer received for this property.")
    offer_count = fields.Integer(string="Offers Count", compute='_compute_offer_count')

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price', 'offer_ids.status')
    def _compute_best_offer(self):
        for record in self:
            accepted_offers = record.offer_ids.filtered(lambda o: o.status == 'accepted')
            if accepted_offers:
                record.best_offer = max(accepted_offers.mapped('price'), default=0)
            else:
                record.best_offer = max(record.offer_ids.mapped('price'), default=0)

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = self.garden_area if self.garden_area > 0 else 10
            self.garden_orientation = self.garden_orientation if self.garden_orientation else 'N'
        else:
            self.garden_area = 0
            self.garden_orientation = False

    _sql_constraints = [
        ('unique_property_title_company', 'UNIQUE(name, company_id)', 'The property title must be unique per company!'),
        ('check_expected_price_positive', 'CHECK(expected_price > 0)', 'The expected price must be strictly positive.'),
        ('check_selling_price_positive', 'CHECK(selling_price >= 0)', 'The selling price must be positive or zero.'),
    ]

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price_not_less_than_90_percent_expected(self):
        for record in self:
            if record.selling_price > 0 and record.expected_price > 0 and record.selling_price < (record.expected_price * 0.9):
                raise ValidationError("Selling price cannot be less than 90% of the expected price.")

    def action_set_to_sold(self):
        self.ensure_one()
        if self.state == 'canceled':
            raise UserError("Canceled properties cannot be set to sold.")
        accepted_offer = self.offer_ids.filtered(lambda o: o.status == 'accepted')
        if not accepted_offer:
            raise UserError("There is no accepted offer for this property. Please accept an offer first.")
        self.selling_price = accepted_offer[0].price
        self.buyer_id = accepted_offer[0].partner_id
        self.state = 'sold'
        return True

    def action_cancel_property(self):
        self.ensure_one()
        if self.state == 'sold':
            raise UserError("Sold properties cannot be canceled.")
        accepted_offers = self.offer_ids.filtered(lambda o: o.status == 'accepted')
        for offer in accepted_offers:
            offer.action_refuse_offer()
        self.state = 'canceled'
        self.selling_price = 0
        self.buyer_id = False
        return True

    def action_view_offers(self):
        self.ensure_one()
        return {
            'name': f"Offers for {self.name}",
            'type': 'ir.actions.act_window',
            'res_model': 'estate.property.offer',
            'view_mode': 'list,form',
            'domain': [('property_id', '=', self.id)],
            'context': {'default_property_id': self.id}
        }
