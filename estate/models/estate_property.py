from datetime import timedelta

from odoo import models, fields, api
from odoo.exceptions import UserError

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    _order = 'id desc'

    name = fields.Char(string="Name", required=True)
    image = fields.Image()
    description = fields.Text(string="Description")
    postcode = fields.Char(string="postcode")
    date_availability = fields.Date(
        string="Date Availability", 
        default=lambda self: fields.Date.today() + timedelta(days=90),
        copy=False
    )
    expected_price = fields.Float(string="Expected Price", default=0, required=True)
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
    property_type_id =fields.Many2one('estate.property.type',string="Property Type", ondelete="cascade")
    salesperson_id = fields.Many2one('res.users', string="Salesperson", default=lambda self: self.env.user)
    buyer_id = fields.Many2one('res.partner', string="Buyer", copy=False)    
    tag_ids = fields.Many2many('estate.property.tag', string="Tag Name", ondelete="cascade")
    offer_ids = fields.One2many('estate.property.offer', "property_id")

    best_price = fields.Float(string="Best Price", compute="_best_price", store=True)
    sequence = fields.Integer('Sequence', default=0)
    company_id = fields.Many2one('res.company', default=lambda self:self.env.company)

    @api.depends("offer_ids")   
    def _best_price(self):      # Commputed Method
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped('price'))
            else:
                record.best_price = 0.0

    
    @api.depends("living_area", "garden_area")
    def _compute_total(self):       # Commputed Method
        for record in self:
            record.total_area = (record.living_area or 0) + (record.garden_area or 0)

    @api.onchange('garden')         # Onchange Method
    def _onchange_garden(self):
        for record in self:
            if record.garden:
                record.garden_area = 10 
                record.garden_orientation = 'north'  
            else:
                record.garden_area = 0  
                record.garden_orientation = False

    def action_to_sold(self):       #   Function
        for record in self:
            if record.state == 'cancelled':
                raise UserError("Cancelled Property can not be sold")
            elif record.state == 'offer accepted':
                self.state = 'sold'

    def action_to_cancel(self):     #   Function
        for record in self:
            if record.state == 'offer accepted':
                record.state = 'cancelled'
                
    _sql_constraints = [
        ('expected_price_positive', 'CHECK(expected_price > 0)', 'Expected Price must be strictly positive!'),
        ('selling_price_positive', 'CHECK(selling_price > 0)', 'Selling Price must be positive!'),
    ]

    @api.constrains('selling_price')
    def _check_lower_selling_price(self):
        for record in self:
            lower_price = (record.expected_price * 9)/10
            if record.selling_price <= lower_price:
                raise UserError("selling Price should be Higher than 90%")

    @api.ondelete(at_uninstall=False)                   # For Delete property using inherit the ondelete()
    def _unlink_if_property_new_and_canclled(self):     # override delete method user can delete user if state is NEW or CANCELLED 
        for record in self:
            if record.state not in ['new', 'cancelled']:
                raise UserError('Only New and Cancelled property can be delete.')

    def action_make_offer(self):
        return {
            'name': ('Make Offers'),
            'type': 'ir.actions.act_window',
            'target': 'new',
            'view_mode': 'form',
            'res_model': 'estate.property.make.offer',
            'context': {
                'default_property_ids': self.env.context.get('active_ids'),
            }
        }
