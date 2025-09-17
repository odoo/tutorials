from odoo import api, fields, models 
from odoo.exceptions import UserError 

class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = "Estate Property"
    
    name = fields.Char(string="Title", required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(string="Available From")
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    type = fields.Many2one('estate.property.type', string="Property Type")
    area = fields.Integer()
    garden = fields.Boolean()
    garden_area = fields.Integer(string="Garden Area")
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West')
    ])
    status = fields.Selection([
        ('new', 'New'),
        ('sold', 'Sold'),
        ('canceled', 'Canceled')], default='new', required=True)
    tag_ids = fields.Many2many(
        'estate.property.tag'
    )
    salesman_id = fields.Many2one(
        'res.users', 
        default=lambda self: self.env.user
    )
    buyer_id = fields.Many2one(
        'res.partner', 
        copy=False
    )
    offer_ids = fields.One2many(
    'estate.property.offer',
    'property_id'
    )
    total_area = fields.Integer(compute="_compute_total_area", store=True)
    best_offer = fields.Float(compute="_compute_best_price", store=True)
    
    @api.depends('area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.area + record.garden_area
       
    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            record.best_offer = max(record.offer_ids.mapped('price'), default=0)
    
    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
            
    def cancelRequest(self):
        self.status = 'canceled'
        
    def action_sold_property(self):
        if self.status == 'canceled':
            raise UserError('Canceled property cannot be sold!')
        self.status = 'sold'
    
    def action_cancel_property(self):
        if self.status == 'sold':
            raise UserError('Sold property cannot be bought!')
        self.status = 'canceled'
