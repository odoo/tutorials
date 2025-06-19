from odoo import fields, models, api
from datetime import timedelta, date

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Store Real Estate Properties"

    name = fields.Char("Estate Name", required=True, translate=True)
    description = fields.Text("Description", help="Enter the real estate item description")
    postcode = fields.Char("Postcode")
    date_availability = fields.Date("Available From", copy=False, default=lambda self: date.today() + timedelta(days=90))
    expected_price = fields.Float("Expected Price", digits=(16, 1))
    selling_price = fields.Float("Selling Price", digits=(16, 1), copy=False, readonly=True)
    bedrooms = fields.Integer("Bedrooms", default=2, help="Number of bedrooms in the property")
    living_area = fields.Integer("Living Area (m²)", default=0)
    facades = fields.Integer("Facades", help="Number of building facades")
    garage = fields.Boolean("Garage", default=False)
    garden = fields.Boolean("Garden", default=False)
    garden_area = fields.Integer("Garden Area (m²)", default=0)
    garden_orientation = fields.Selection(
        [
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')
        ],
        string="Garden Orientation",
        help="Direction the garden faces"
    )
    active = fields.Boolean("Active", default=True)
    state = fields.Selection([
        ('new', 'New'),
        ('offer_received', 'Offer Received'),
        ('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('cancelled', 'Cancelled'),
    ], copy=False, default="new")
    
    # Computed fields
    total_area = fields.Float(compute="_compute_total_area")
    best_price = fields.Float(string="Best Offer", compute="_compute_best_price")

   

    
    # Computed functions
    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area
    
    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            prices = record.offer_ids.mapped("price")
            record.best_price = max(prices) if prices else 0.0
            
    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False
            
    # Relations
    property_type_id = fields.Many2one('estate.property.type', string="Property Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    salesperson_id = fields.Many2one("res.users", string="Salesperson", default=lambda self: self.env.user)
    tag_ids = fields.Many2many("estate.property.tag", string="Property Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")

    note = fields.Text("Special mentions about the house")
