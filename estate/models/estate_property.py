from odoo import fields, models, api
from odoo.tools.populate import compute


# 
#  Base Property Model
# 

class Property(models.Model):
    # Model Properties
    _name = "estate.property"
    _description = "Estate properties" 
    
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
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string = 'Garden Orientation',
        selection = [('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
    )
    state = fields.Selection(
        string = 'Status',
        selection = [('new', 'New'), ('offerreceived', 'Offer Received'), ('offeraccepted', 'Offer Accepted'), ('sold', 'Sold'),('canceled', 'Canceled')],
        default='new',
        copy=False,
    )
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
            property.best_price = max(property.offer_ids.mapped('price'))
            
