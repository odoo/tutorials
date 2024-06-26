from odoo import fields, models, api, exceptions
from odoo.tools.float_utils import float_compare
from odoo.tools.populate import compute


# 
#  Base Property Model
# 

class Property(models.Model):
    # Model Properties
    _name = "estate.property"
    _description = "Estate properties" 
    
    # 
    # SQL Constraints
    # 
    _sql_constraints=[
        ('expected_price', 'CHECK(expected_price > 0)', 'expected price must be positive'),
        ('selling_price', 'CHECK(selling_price >= 0)', 'Selling price must be positive'),
        ('name', 'unique(name)', 'The name must be unique'),
    ]
    
    #
    # Fields
    #
    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(string='Availible From',copy=False, default=fields.Date.add(fields.Date.today(), months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string='Living area (sqm)')
    facades = fields.Integer()
   
    # 
    # On Change
    # 
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string = 'Garden Orientation',
        selection = [('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
    )
    
    @api.onchange("garden")
    def _onchange_garden(self):
        for record in self:    
            if record.garden:
                record.garden_area = 10
                record.garden_orientation = 'north'
            else:
                record.garden_area = 0
                record.garden_orientation = ''
    
    # 
    # Actions
    # 
    state = fields.Selection(
        string = 'Status',
        selection = [('new', 'New'), ('offerreceived', 'Offer Received'), ('offeraccepted', 'Offer Accepted'), ('sold', 'Sold'),('canceled', 'Canceled')],
        default='new',
        copy=False,
    )
    def property_action_cancel(self):
        for property in self:
            if (property.state == 'sold' or property.state == 'canceled'):  
                raise exceptions.UserError("Property can't be sold if it's already sold or canceled")
            else:
                property.state = 'canceled'


    def property_action_sold(self):
        for property in self:
            if (property.state == 'sold' or property.state == 'canceled'):
                raise exceptions.UserError("Property can't be sold if it's already sold or canceled")
            else:
                property.state = 'sold'
    

    
    active = fields.Boolean(default=True)
    # Property Types
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    
    # Buyer seller 
    salesman_id = fields.Many2one("res.users", string ='Salesman', default=lambda self: self.env.user)
    buyer_id = fields.Many2one("res.partner", string ='Buyer', copy=False)
    
    # Tags
    tag_ids = fields.Many2many("estate.property.tag", string="Property Tags")
    
    # Offer
    offer_ids = fields.One2many("estate.property.offer", "property_id")
    @api.onchange('offer_ids')
    def _property_action_offer_received(self):
        for property in self:
            if(len(property.offer_ids) > 0):
                property.state = 'offerreceived'
            else:
                property.state = 'new'
    # 
    # Calculations
    # 
    total_area = fields.Integer(compute='_calc_total_area')
    @api.depends("garden_area", 'living_area')
    def _calc_total_area(self):
        for property in self:
            property.total_area = property.garden_area + property.living_area
            
    best_price = fields.Float(compute="_calc_best_price")
    @api.depends('offer_ids.price')
    def _calc_best_price(self):
        for property in self:
            if (len(property.offer_ids) > 0):
                property.best_price = max(property.offer_ids.mapped('price'))
            else:
                property.best_price = 0
            
    # 
    #  Api constraints
    # 
    @api.constrains('selling_price')
    def _check_selling_price(self):
        for property in self:
            if float_compare(property.selling_price, property.expected_price * 0.9, precision_digits=2) < 0 and property.selling_price > 0:
                raise exceptions.ValidationError("Selling price must be higher than 90% of expected price")
