from odoo import models, fields
from datetime import timedelta, date
from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"
    name = fields.Char(required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(copy=False, default=lambda self: date.today() + timedelta(days=90))
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price")
    bedrooms = fields.Integer(default=2)
    active = fields.Boolean(default=True)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage Available")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
            ('north', "North"),
            ('south', "South"),
            ('east', "East"),
            ('west', "West")
        ]
    )    
    state = fields.Selection([
        ('new', 'New'),
        ('sold', 'Sold'),
        ('refused', 'Refused')
    ], string="Status",required=True, default='new')
    property_type_id = fields.Many2one('estate.property.type', string="Property Type") 
    buyer_id = fields.Many2one('res.partner', string="Buyer")
    seller_id = fields.Many2one('res.users', string="Salesperson", default=lambda self: self.env.user)
    # name = fields.Char(string="Tag", required=True)
    status = fields.Selection([('accepted', 'Accepted'), ('refused', 'Refused')], string="Status")
    partner_id = fields.Many2one('res.partner', string="Partner", required=True)
    salesperson = fields.Char(string = "Salesperson", required=True)
    buyer = fields.Char(string = "Buyers", required=True)
    price = fields.Float(string="Price")
    partners = fields.Char(string = "Partner", required=True)
    tag = fields.Many2one('estate.property.tag' , string="Tags") 
    total_area = fields.Float(string="Total Area (sqm)", compute="_compute_total_area", store=True,copy=False)
    best_offers = fields.Float(string="Best Offers")
    offer_ids = fields.One2many(
        'estate.property.offer', 
        'property_id', 
        string="Offers"
    )
    validity = fields.Integer(string="Validity (days)")
    date_deadline = fields.Date(
        string="Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
        store=True)
    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False
    tag_ids = fields.Many2many(
        'estate.property.tag',
        string='Tags'
    )
    def action_cancel(self):
        for record in self:
            if record.state == 'sold':
                raise UserError("A sold property cannot be cancelled.")
            record.state = 'cancelled'

    def action_sold(self):
        for record in self:
            if record.state == 'cancelled':
                raise UserError("A cancelled property cannot be sold.")
            record.state = 'sold'
    
    sql_constraints = [
        ('expected_price_positive', 'CHECK(expected_price > 0)',
         'The expected price must be strictly positive.'),
        ('selling_price_positive', 'CHECK(selling_price >= 0)',
         'The selling price must be positive.')
    ]
    @api.constrains('expected_price')
    def _check_expected_price(self):
     for record in self:
        if record.expected_price <= 0:
            raise ValidationError("The expected price must be strictly positive.")
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string="Offers")
    best_price = fields.Float(string="Best Price", compute="_compute_best_price", store=True)

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped('price'), default=0)
     
    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = (record.living_area or 0) + (record.garden_area or 0)                    