from datetime import timedelta

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate property'
    _inherit = ['mail.thread']
    _order = 'id desc'

    name = fields.Char(string='Name', required=True, tracking=True)
    description = fields.Text(string='Description')
    postcode = fields.Char(string='Postcode',size=6)
    date_availability = fields.Date(string='Available From', default=(fields.Date.today() + timedelta(days=90)), copy=False)
    expected_price = fields.Float(string='Expected Price')
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
        ], string='Garden Orientation')
    state = fields.Selection([
        ('new', 'New'),
        ('offer_received', 'Offer Received'),
        ('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('cancelled', 'Cancelled')
        ], string='State', default='new', tracking=True)
    active = fields.Boolean(default=True)
    property_type_id = fields.Many2one('estate.property.type', string='Property Type')
    salesman_id = fields.Many2one('res.users', string='Salesman', default=lambda self: self.env.user)
    buyer_id = fields.Many2one('res.partner', string='Buyer', copy=False)
    tag_ids = fields.Many2many('estate.property.tag',string='Tags')
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offer')
    total_area = fields.Float(string='Total Area (sqm)', compute='_compute_total_area')
    best_offer = fields.Float(string='Best Offer', compute='_compute_best_price')
    reference = fields.Char(string="Reference", copy=False, readonly=True)
    company_id = fields.Many2one('res.company', string='Company Name', default=lambda self: self.env.company, required=True)

    _sql_constraints = [('expected_price_check', 'CHECK(expected_price >= 0)', 'Expected price must be strickly possitive.'),
                        ('selling_price_check', 'CHECK(selling_price >= 0)', 'Selling price must be possitive.')]

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area
    
    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            record.best_offer = max(record.offer_ids.mapped('price'), default=0)

    @api.onchange('garden')
    def onchange_garden_available(self):
        if self.garden == True:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('state') == 'new':
                vals['reference'] = self.env['ir.sequence'].next_by_code('estate.property') or 'New'
        return super().create(vals_list)

    def sold_action(self):
        for record in self:
            if record.state == 'cancelled':
                raise UserError("Cancelled properties cannot be sold.")
            record.state = 'sold'

    def cancel_action(self):
        for record in self:
            if record.state == 'sold':
                raise UserError("sold properties cannot be cancelled.")
            record.state = 'cancelled'
                
    @api.constrains('selling_price', 'expected_price')
    def check_range_selling_price(self):
        for record in self:
            if record.selling_price > 0 and record.expected_price * 0.9 > record.selling_price:
                raise ValidationError("Selling price is less than 90% of expected price. you must have set selling price more than 90% of expected price.")

    @api.ondelete(at_uninstall=False)
    def _unlink_except_property(self):
            for record in self:
                if record.state not in ['new', 'cancelled']:
                    raise UserError("You cannot delete offer, when it's in %s state.", record.state)

    def _track_subtype(self, vals):
        self.ensure_one()
        if 'state' in vals and self.state == 'offer_accepted':
            return self.env.ref('estate.mt_state_change')
        return super()._track_subtype(vals)
