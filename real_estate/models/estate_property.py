from odoo import models, fields, api
from odoo.exceptions import UserError  # यह लाइन जोड़ें

from datetime import date

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(string="Available From", default=lambda self: date.today())
    expected_price = fields.Float(required=True)
    selling_price = fields.Float()
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    total_area = fields.Float(string="Total Area (sqm)", compute="_compute_total_area", store=True)
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    best_price = fields.Float(string="Best Offer Price", compute="_compute_best_price", store=True)

    status = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused'),
    ], string="Status", default="accepted")

    state = fields.Selection([
    ('new', 'New'),
    ('offer_received', 'Offer Received'),
    ('offer_accepted', 'Offer Accepted'),
    ('sold', 'Sold'),
    ('canceled', 'Canceled')  # यह एंट्री होनी चाहिए
], string="Status", default="new")



    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West'),
    ], string="Garden Orientation")

    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    salesperson_id = fields.Many2one("res.users", string="Salesperson", default=lambda self: self.env.user)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
   

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    
    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped("price"), default=0)

    @api.onchange('garden')
    def _onchange_garden(self):
     
        if self.garden:
            self.garden_area = 10
            self.garden_orientation= 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False
  
    
    def action_cancel(self):
        """Cancels the property if not sold"""
        if self.state == 'sold':
            raise UserError("You cannot cancel a sold property.")
        self.state = 'cancelled'

    def action_sold(self):
        """Marks the property as sold if not cancelled"""
        if self.state == 'cancelled':
            raise UserError("You cannot sell a cancelled property.")
        if not self.buyer_id or not self.selling_price:
            raise UserError("Buyer and Selling Price must be set before marking as sold.")
        self.state = 'sold'