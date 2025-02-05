from odoo import fields, models, api
from odoo.exceptions import UserError , ValidationError

class EstateProperty(models.Model):

   
    _name = "estate.property"
    _description = "Test Property"
    

    name = fields.Char(required=True,string="Title")
    salesman = fields.Many2one('res.users', string="Salesman")
    buyer = fields.Many2one('res.partner', string="Buyer",readonly=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()  
    active = fields.Boolean(default=True)
    garage = fields.Boolean()
    garden = fields.Boolean(default=True)
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[
           ('north', 'North'),
           ('south', 'South'),
           ('west', 'West'),
           ('east', 'East')
        ]
    )
    state = fields.Selection(
        string='State',
        required=True,
        store=True,
        copy=False,
        default='new',
        selection=[
            ('new','New'),
            ('offer_received','Offer Received'),
            ('offer_accepted','Offer  Accepted'),
            ('sold','Sold'),
            ('cancelled','Cancelled')
        ]   
    ) 
    property_type_id = fields.Many2one(
        'estate.property.type',  
        string="Property Type",    
    )  
    tags_ids = fields.Many2many(
        "estate.property.tag",
        string="Property Tag"
    )  
    offer_ids = fields.One2many(
        "estate.property.offer",'property_id',
        string="Property Offer",
    ) 
    total_area = fields.Float(
        string="Total Area (sq.m)",
        compute="_compute_total_area",
        store=True
    )
    best_offer = fields.Float(
        string="Best Offer",
        compute="_compute_best_offer",
        store=True
    ) 
 

    _sql_constraints = [        
        ('check_selling_price', 
         'CHECK(selling_price >= 0)', 
         'The selling price must be positive!'),
         ('check_expected_price', 
         'CHECK(expected_price > 0)', 
         'The expected price must be strictly positive!'),
        ('unique_property_name', 
         'UNIQUE(name)', 
         'The property name must be unique!')
    ] 
    _order = "id desc"

    # @api.depends('offer_ids.status')
    # def _compute_state_from_accepted_offer(self):
    #     for property in self:
    #         if any(offer.status == 'accepted' for offer in property.offer_ids):
    #             property.state = 'offer_accepted'
  
    @api.depends('garden_area', 'living_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area
    
    @api.depends('offer_ids.price')
    def _compute_best_offer(self):
        for record in self:
            record.best_offer = max(record.offer_ids.mapped('price'), default=0.0)

    @api.onchange('garden')
    def _onchange_garden(self):
        for record in self:
            if record.garden:
                record.garden_area = 10
                record.garden_orientation = 'north'
            else:
                record.garden_area = 0
                record.garden_orientation = False 
    
    def action_cancel(self):  
        for record in self:
            if record.state == 'sold':
                raise UserError("Sold properties cannot be canceled.")
            record.state='cancelled'

    def action_sold(self):
        for record in self:
            if record.state == 'cancelled':
                raise UserError("Canceled properties cannot be sold.")
            record.state = 'sold' 
    
    @api.constrains('selling_price')
    def _check_selling_price(self):
        for record in self:
            if record.selling_price and record.selling_price < record.expected_price * 0.9:
                raise ValidationError(
                    "The selling price cannot be lower than 90% of the expected price."  
                ) 

    @api.ondelete(at_uninstall=False)
    def _ondelete_check_state(self):
        for record in self:
            if record.state not in ('new', 'cancelled'):
                raise UserError(
                    "You cannot delete a property that is not in 'New' or 'Cancelled' state."
                )   
    

