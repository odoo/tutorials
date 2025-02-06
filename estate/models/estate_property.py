from ast import If
from odoo import api, models, fields
from datetime import datetime
from dateutil.relativedelta import relativedelta

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"

    def calculate_three_months_later():
        today = datetime.now()

        return today + relativedelta(months=3)

    # Fields of Property
    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(string="Date Availability", default=calculate_three_months_later(), copy=False)
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area")
    
    # Garden Orientation of Property
    garden_orientation = fields.Selection(
        string="Garden Orientation", 
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')]);
    
    active = fields.Boolean(string="Is Active", default=True)
    
    # State Selection of Property
    state = fields.Selection(
        string="State", 
        required=True, 
        copy=False,
        default="new",
        selection=[('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'), ('cancelled', 'Cancelled')])

    # Many2one Fields
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")

    salesman = fields.Many2one("res.users", string="Salesman", default=lambda self: self.env.user)
    buyer = fields.Many2one("res.users", string="Buyer", copy=False)

    # Many2many Field
    property_tag_ids = fields.Many2many("estate.property.tag", string="Property Tags")

    # One2many Field
    property_offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")

    # Computed Fields
    total_area = fields.Integer(string="Toatal Area (sqm)", compute="_compute_total_area")
    best_offer = fields.Float(string="Best Offer", compute="_compute_best_offer")

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('property_offer_ids')
    def _compute_best_offer(self):
        for record in self:
            if record.property_offer_ids:
                record.best_offer = max(record.property_offer_ids.mapped('price'), default=0)
            else:
                record.best_offer = 0

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:    
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = None