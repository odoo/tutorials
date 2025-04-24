from odoo import fields, models, api
from dateutil.relativedelta import relativedelta

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"

    name = fields.Char(required = True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=lambda self: fields.Date.today() + relativedelta(months=3))
    expected_price = fields.Float()
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
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
    active = fields.Boolean(default=True)
    state = fields.Selection([
        ('new', 'New'),
        ('offer_received', 'Offer Received'),
        ('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('canceled', 'Cancelled')
    ], required=True, copy=False, default='new')
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    sales_person = fields.Many2one("res.users", string = "Salesman", default = lambda self: self.env.user)
    buyer = fields.Many2one("res.partner", string = "Buyer", copy=False)
    tags = fields.Many2many("estate.property.tag", string = "Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    total_area = fields.Float(string = "Total area", compute="_compute_total_area", store = True)
    best_price = fields.Float(string = "Best Offer", compute= "_compute_best_offer", store = True)
    
    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self: 
            record.total_area = record.living_area + record.garden_area
    
    @api.depends('offer_ids')
    def _compute_best_offer(self):
        for record in self:
            prices = record.offer_ids.mapped('price')
            record.best_price = max(prices) if prices else 0.0
    
    @api.onchange('garden')
    def _onchange_garden(self):
        for record in self:
            record.garden_area = record.garden * record.garden_area