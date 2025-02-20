# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import timedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    _order = "id desc"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _sql_constraints = [
        ('expected_price_positive', 'CHECK(expected_price >= 1)', 'The expected price must be strictly positive.'),
        ('selling_price_positive', 'CHECK(selling_price >= 1)', 'The selling price must be strictly positive.')
    ]

    name = fields.Char(string="Name", required=True)
    active = fields.Boolean(string="Active", default=True)
    state = fields.Selection([
        ('new', 'New'), 
        ('offer_received', 'Offer Received'), 
        ('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold'), 
        ('cancelled', 'Cancelled')
    ], default="new", string="State", tracking=True)
    last_seen = fields.Datetime(string="Last Seen", default=fields.Datetime.now)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(string="Available from", copy=False, default=fields.Date.today() + timedelta(days=+90))
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False) 
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area")
    garden_orientation = fields.Selection([
        ('north', 'North'), 
        ('south', 'South'), 
        ('east', 'East'), 
        ('west', 'West')
    ], string="Garden Orientation", help="Orientation of the garden")  
    total_area = fields.Integer(string="Total Area", compute="_compute_total_area")
    best_offer = fields.Integer(string="Best Offer", compute="_compute_best_offer")
    sequence = fields.Char(string="Sequence", readonly=True, copy=False)
    image = fields.Image(string="Property Image") 
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    seller_id = fields.Many2one("res.users", string="Salesperson", default=lambda self: self.env.user)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    company_id = fields.Many2one("res.company", string="Company", required=True, default=lambda self: self.env.company)

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids')
    def _compute_best_offer(self):
        for record in self:
            record.best_offer = max(record.offer_ids.mapped('price')) if record.offer_ids else 0

    @api.constrains('selling_price', 'expected_price')
    def _check_sellings_price(self):
        for record in self:
            if record.selling_price and record.selling_price < record.expected_price * 0.9:
                raise ValidationError(_("Selling price cannot be lower than 90% of the expected price."))

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden == True:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False
    @api.model_create_multi
    def create(self, vals):
        for val in vals:
            val['sequence'] = self.env['ir.sequence'].next_by_code('estate.property') or 'PROP001'
        return super().create(vals)

    @api.ondelete(at_uninstall=False)
    def _unlink_property(self):
        for record in self:
            if record.state not in ['new', 'cancelled']:
                raise UserError(_("Only New or cancelled properties can be deleted."))

    def action_sold(self):
        for record in self:
            if record.state == 'cancelled': 
                raise UserError(_("Cancelled properties cannot be sold"))
            else: 
                record.state = 'sold'

    def action_cancelled(self):
        for record in self:
            if record.state == 'sold': 
                raise UserError(_("Sold properties cannot be cancelled"))
            else:
                record.state = 'cancelled'
                
    def _track_subtype(self, init_values):
        self.ensure_one()
        if 'state' in init_values and self.state == 'offer_accepted':
            return self.env.ref('estate.mt_state_change')
        return super()._track_subtype(init_values)
