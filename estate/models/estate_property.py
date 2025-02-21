from dateutil.relativedelta import relativedelta

from odoo import fields, models, api
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare, float_is_zero


class Property(models.Model):
    _name = "estate.property"
    _description = "Real Estate Properties"
    _order = "id desc"
    
    _sql_constraints = [
        ('check_prices', 'CHECK(expected_price > 0 AND selling_price >= 0)',
         "Prices should be positive. Additionnaly, expected price can't be 0.")
    ]
    
    # Metadata
    name = fields.Char('Title', required=True, translate=True, default="Best House In Town")
    active = fields.Boolean(default=True)
    description = fields.Text('Description', default="Yo yo yo, no dup for date and status !")
    postcode = fields.Char('Postcode', translate=True)
    property_type_id = fields.Many2one('estate.property.type', string='Type')
    property_tag_ids = fields.Many2many('estate.property.tag', string='Tags')
    property_offer_ids = fields.One2many('estate.property.offer', 'property_id')    
    
    # House Data
    bedrooms = fields.Integer('Bedrooms', default=2)
    living_area = fields.Integer('Living Area (sqm)')
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Garage', default=False)
    garden = fields.Boolean('Garden', default=False)
    garden_area = fields.Integer('Garden Area (sqm)')
    garden_orientation = fields.Selection(
        string='Garden Orientation', 
        selection = [
            ('north', "North"), 
            ('south', 'South'), 
            ('east', 'East'), 
            ('west', 'West')
        ]
    )
    total_area = fields.Integer('Total Area (sqm)', compute="_compute_total_area")
    
    # Business things
    date_availability = fields.Date('Available From', copy=False, default=lambda self: fields.Date.today() + relativedelta(months=3))
    expected_price = fields.Float('Expected price', required=True)
    selling_price = fields.Float('Selling Price', readonly=True, copy=False)
    best_price = fields.Float('Best Price', compute="_compute_best_price")
    buyer = fields.Many2one('res.partner', string='Buyer')
    salesperson = fields.Many2one('res.users', string='Salesperson')
    state = fields.Selection(
        string='State',
        selection = [
            ('new', "new"), 
            ('offer_received', 'Offer Received'), 
            ('offer_accepted', 'Offer Accepted'), 
            ('sold', 'Sold'), 
            ('cancelled', 'Cancelled')
        ],
        default='new'
    )
    
    # Functions
    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area
            
    @api.depends("property_offer_ids")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.property_offer_ids.mapped('price')) if record.property_offer_ids else 0.0
            
    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_orientation = 'north'
            self.garden_area = 10
        else:
            self.garden_orientation = False
            self.garden_area = 0
    
    def action_reset(self):
        if self.state != 'cancelled':
            raise UserError("You can only reset a cancelled property")
        
        self.state = 'new'
    
    def action_cancel(self):
        if self.state == 'sold':
            raise UserError("You cannot cancel a sold property")
        
        if self.state == 'cancelled':
            raise UserError("Property already cancelled")
        
        self.state = 'cancelled'
    
    def action_sold(self):
        if self.state == 'cancelled':
            raise UserError("You cannot sell a cancelled property")
        
        if self.state == 'sold':
            raise UserError("Property already sold")
        
        if self.state != 'offer_accepted':
            raise UserError("Can't sell a property without an accepted offer")
        
        self.state = 'sold'
    
    # Called by offer.action_accept
    def action_accept_offer(self, offer_to_accept_id):
        if self.state == 'cancelled':
            raise UserError("You cannot accept an offer on a cancelled property")
        
        if self.state == 'cancelled':
            raise UserError("You cannot accept an offer on a sold property")
        
        offer_to_accept_id.accept()
        self.state = 'offer_accepted'
    
    # Called by offer.action_accept
    def action_refuse_offer(self, offer_to_accept_id):
        if self.state == 'cancelled':
            raise UserError("You cannot refuse an offer on a cancelled property")
        
        if self.state == 'cancelled':
            raise UserError("You cannot refuse an offer on a sold property")
        
        offer_to_accept_id.refuse()
        self.state = 'new'
        for offer in self.property_offer_ids:
            if offer.status == 'accepted': # Some accepted offer exists
                self.state = 'offer_received'
                return
            elif offer.status != 'refused': # Some neutral offer exists
                self.state = 'offer_received'
    
    @api.constrains('selling_price', 'expected_price')
    def check_selling_price(self):
        for record in self:
            if not float_is_zero(record.selling_price, precision_digits=3) and float_compare(record.selling_price, 0.9 * record.expected_price, precision_digits=3) < 0:
                raise UserError('Selling price is too low')
    
    @api.ondelete(at_uninstall=False)
    def _unlink_restrictions(self):
        for record in self:
            if record.state not in ['new', 'cancelled']:
                raise UserError("You only delete new and cancelled properties")




