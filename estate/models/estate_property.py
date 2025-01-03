from odoo import models, fields, api, exceptions
from datetime import timedelta

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"

    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="postcode")
    date_availability = fields.Date(
        string="Date Availability", 
        default=lambda self: fields.Date.today() + timedelta(days=90),
        copy=False
    )
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price", readonly=True)
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garge")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area")
    total_area = fields.Float(string="Total Area", compute="_compute_total", store=True)
    garden_orientation = fields.Selection(
        [
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')
        ],
        string="Garden Orientation"
    )
    active = fields.Boolean(string="Active", default=True)
    state = fields.Selection(
        [
            ('new', 'New'),
            ('offer received', 'Offer Received'),
            ('offer accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled')
        ],
        string="Status",
        default='new',
        required=True
    )
    property_type_id =fields.Many2one('estate.property.type',string="Property Type")
    salesperson_id = fields.Many2one('res.users', string="Salesperson", default=lambda self: self.env.user)
    buyer_id = fields.Many2one('res.partner', string="Buyer", copy=False)    
    tag_ids = fields.Many2many('estate.property.tag', string="Tag Name")
    offer_ids = fields.One2many('estate.property.offer', "property_id", ondelete='restrict')

    best_price = fields.Float(string="Best Price", compute="_best_price", store=True)

    @api.depends("offer_ids")
    def _best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped('price'))
            else:
                record.best_price = 0.0

    
    @api.depends("living_area", "garden_area")
    def _compute_total(self):
        for record in self:
            record.total_area = (record.living_area or 0) + (record.garden_area or 0)

    @api.onchange('garden')
    def _onchange_garden(self):
        for record in self:
            if record.garden:
                record.garden_area = 10 
                record.garden_orientation = 'north'  
            else:
                record.garden_area = 0  
                record.garden_orientation = ''

    def action_to_sold(self):
        for record in self:
            if record.state == 'cancelled':
                raise exceptions.UserError("Cancelled Property can not be sold")
            elif record.state == 'new':
                self.state = 'sold'

    def action_to_cancel(self):
        for record in self:
            if record.state == 'new':
                record.state = 'cancelled'




