from odoo import api, fields, models
from datetime import timedelta

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property Name"

    name = fields.Char('Property Name', required = True, size = 30)
    description = fields.Text('Description', size = 50)
    postcode = fields.Char('Postcode', size = 6)
    date_availability = fields.Date('Date Availability',default=fields.Date.today() + timedelta(days=90), copy=False)
    expected_price = fields.Float('Expected Price', required = True)
    selling_price = fields.Integer('Selling Price', 
        readonly=True, 
        copy=False,
        default=1000000
    )
    bedrooms = fields.Integer('Bedrooms', default = "2")
    living_area = fields.Integer('Living Area')
    facades = fields.Integer('Facedes')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden', default=False)
    garden_area = fields.Integer('Garden Area(sqm)', default = 0)
    total_area = fields.Integer('Total Area (sqm)', compute="_compute_total_area", store=True)
    garden_orientation = fields.Selection(
        string ='Type',
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')    
        ]
    )
    active = fields.Boolean('Active', 
        default=True, 
        help='if you want to active'
        )
    state = fields.Selection(
        required = True,
        copy = False,
        default = "new",
        selection = [
            ('new', 'New'),
            ('offer received', 'Offer Received'),
            ('offer accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled')
        ]
    )
    salesman_id = fields.Many2one('res.users',default=lambda self: self.env.user, string='Salesman')
    buyer_id = fields.Many2one('res.partner', string='Buyer', copy=True)
    tags_ids = fields.Many2many('estate.property.tag', string='Tags')
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    best_price = fields.Float(string="Best Offer", compute="_compute_best_price", store=True)

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area
    
    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped("price"), default=0.0)

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False