from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models

from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"
    
    name = fields.Char("Property Name", required=True)
    description = fields.Text("Description")
    postcode = fields.Char("Postcode")
    date_availability = fields.Date("Available From", copy=False, default=fields.Date.today() + relativedelta(months=3))
    expected_price = fields.Float("Expected Price", required=True)
    selling_price = fields.Float("Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer("Bedrooms", default=2)
    living_area = fields.Integer("Living Area (sqm)")
    facades = fields.Integer("Facades")
    garage = fields.Boolean("Garage")
    garden = fields.Boolean("Garden")
    garden_area = fields.Integer("Garden Area (sqm)")
    active = fields.Boolean(default=True)
    garden_orientation = fields.Selection( 
        string="Garden Orientation",
        selection=[
            ('north', 'North'), 
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West'),
        ],
    )
    state = fields.Selection(
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled'),
        ],
        required=True, copy=False, default='new',
    )
    property_type_id = fields.Many2one('estate.property.type', string="Property Type")
    user_id = fields.Many2one('res.users', string="Salesman", default=lambda self: self.env.user)
    partner_id = fields.Many2one('res.partner', string="Buyer", copy=False)
    tag_ids=fields.Many2many('estate.property.tag', string="Tags")
    offer_ids=fields.One2many('estate.property.offer', 'property_id', string='Offers')
    total_area = fields.Integer(string='Total Area (sqm)', compute='_compute_total_area')
    best_price = fields.Float(string='Best Offer', compute='_compute_best_offer')

    _sql_constraints=[
        ('check_expected_price', 'CHECK(expected_price > 0)', 'Expected price must be strickly possitive.'),
        ('check_selling_price', 'CHECK(selling_price >= 0)', 'Selling price must be possitive.'),
    ]

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
    
    def property_sold_action(self):
        for record in self:
            if record.state == 'cancelled':
                raise UserError("Cancelled properties cannot be sold.")
            record.state = 'sold'

    def property_cancel_action(self):
        for record in self:
            if record.state == 'sold':
                raise UserError("sold properties cannot be cancelled.")
            record.state = 'cancelled'

    @api.constrains('selling_price','expected_price')
    def check_selling_price(self):
        for record in self:
            if not float_is_zero(record.selling_price, precision_digits=1) and float_compare(record.selling_price, 0.9 * record.expected_price, precision_digits=1) == -1:
                raise ValidationError('The selling price must be at least 90% of the expected price! You must reduce expected price if you want to accept this offer')
