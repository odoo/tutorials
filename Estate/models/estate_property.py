
from odoo import models, fields , api 
from datetime import timedelta


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    create_date = fields.Date()
    expected_price = fields.Float(required=True)
    selling_price = fields.Float()
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West'),
    ])
    state = fields.Selection(
        [
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('canceled', 'Canceled'),
        ],
        string="Status",
        required=True,
        copy=False,
        default='new'
    )
    active = fields.Boolean(default=True)
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")        
    buyer_id = fields.Many2one("res.partner", string="Buyer")
    salesperson_id = fields.Many2one("res.users", string="Salesperson")
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    total_area = fields.Float(compute="_compute_total_area", string="Total Area", store=True)
    best_price = fields.Float(compute="_compute_best_price", string="Best Offer", store=True)
    validity_days = fields.Integer(default=7)
    deadline_date = fields.Date(compute="_compute_validity_date", string="Validity Date", store=True)
    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + (record.garden_area or 0)  
    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped('price'))
            else:
                record.best_price = 0.0
    
    @api.depends('create_date', 'validity_days')
    def _compute_validity_date(self):
        if  self.create_date:
            for record in self:
                record.deadline_date = record.create_date + timedelta(days=record.validity_days)
        else:
            for record in self:
                record.deadline_date = fields.Date.today() + timedelta(days=record.validity_days)   

    @api.onchange('garden_area')
    def  _onchange_garden(self):   
        for record in self:
            if self.garden_area == 10:
                self.garden_orientation = 'north'
            if self.garden_area == 20:  
                self.garden_orientation = 'south'
            if self.garden_area == 30:
                self.garden_orientation = 'east'
            if self.garden_area == 40:
                self.garden_orientation = 'west'
            else:
                self.garden_area = 0
                self.garden_orientation = False