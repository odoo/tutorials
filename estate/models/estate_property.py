from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo import models, fields, api
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "This is a estate property app"
    
    @api.depends("garden_area","living_area")
    def _compute_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area
            
    @api.depends('offer_ids')
    def _compute_best_offer(self):
        for record in self:
            if(record.offer_ids):
                record.best_offer = max(record.offer_ids.mapped('price'))
            else:
                record.best_offer = 0
    
    @api.onchange('is_garden')
    def _onchange_garden(self):
        if(self.is_garden is True):
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area=0
            self.garden_orientation = ''   

    def sold_property(self):
        for record in self:
            if(record.status == 'cancelled'):
               raise UserError('Cancelled property cannot be sold')
            else:
                record.status='sold'
        
    def cancel_property(self):
        for record in self:
            if(record.status == 'sold'):
                raise UserError('Sold property cannot be cancelled')
            else:
                record.status='cancelled'
            
    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        default=fields.Date.today() + relativedelta(months=3), copy=False
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    best_offer = fields.Integer(readonly=True, compute='_compute_best_offer')
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    is_garage = fields.Boolean("Garage")
    is_garden = fields.Boolean("Garden")
    garden_area = fields.Integer()
    total_area = fields.Integer(compute = '_compute_area', readonly=True)
    property_type_id = fields.Many2one('estate.property.type', string='Property Type')
    salesman_id = fields.Many2one('res.users', default=lambda self: self.env.user)
    buyer_id = fields.Many2one('res.partner', copy=False)
    tag_ids = fields.Many2many('estate.property.tag', string='Tags')
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offer')
    garden_orientation = fields.Selection(
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
        default='north',
    )
    active = fields.Boolean(default=True)
    status = fields.Selection(
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        default="new",
    )
