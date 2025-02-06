from odoo import api, fields, models
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError

class estateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Real Estate Property'

   
   

    # Basic fields for property details
    name = fields.Char(string="Property name", required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(
        string="Availability Date",
        default=lambda self: fields.Date.today() + relativedelta(months=3)  
    )
    

    # to add a buyer and seller field in our form beacuse of the buyer can be anyone one but the seller must be the employer or the seller owner
    buyer_id=fields.Many2one('res.partner', string="buyer" , required=False)
    salesperson_id=fields.Many2one('res.users', string='sales_person_name' , default= lambda self: self.env.user, required=True)

    expected_price = fields.Float(string="Expected Price", required=True, default=0.0)
    selling_price = fields.Float(string="Selling Price", readonly=True)  
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area (sq.m.)")
    facades = fields.Integer(default=3)
    validity = fields.Integer(string="Validity", default=7)
    date_deadline = fields.Date(string='Date Deadline')
    garage = fields.Boolean(string="Has Garage")
    garden = fields.Boolean(string="Has Garden")
    garden_area = fields.Integer(string="Garden Area (sq.m.)")
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('new', 'new'),
        ('offer received','offer received'),
        ('east', 'East'),
        ('west', 'West')
    ], string='Garden Orientation')

    state = fields.Selection(
        [
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled')
        ],
        default='new',
        required=True,
        copy=False,
     )
    active = fields.Boolean(default=True)  

     #  to use a compute decorator
    living_area=fields.Float(string="living_area")
    garden_area=fields.Float(string="garden_area")
    total_area=fields.Float(string="total_area", compute='compute_total_area', store=True)

    @api.depends('living_area', 'garden_area')
    def compute_total_area(self):
        for record in self:
            record.total_area=record.living_area+record.garden_area

   
    # we have add the many relation ship of model
    property_type_id = fields.Many2one('estate.property.type', string="Property Type")
    tag_ids=fields.Many2many('estate.property.tag', string="Tags")
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string="Offers")
    best_price = fields.Float(string="Best Price", compute="_compute_best_price", store=True)

    #  we have to add the best price decorated to use to show the best price in our field
    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            # Get the maximum price from all related offers using mapped
            best_offer = max(record.offer_ids.mapped('price'), default=0.0)
            record.best_price = best_offer



    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10  
            self.garden_orientation= 'north'  
        else:
            self.garden_area = False  
            self.garden_orientation= False

    # Button actions
    def action_cancel(self):
        for record in self:
            if record.state == 'sold':
                raise UserError('A sold property cannot be cancelled.')
            record.state = 'cancelled'

    def action_sold(self):
        for record in self:
            if record.state == 'cancelled':
                raise UserError('A cancelled property cannot be sold.')
            record.state = 'sold'
