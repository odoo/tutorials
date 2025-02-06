from odoo import api, fields, models
from dateutil.relativedelta import relativedelta


class EstateProperty(models.Model):

    _name = 'estate.property'
    _description = 'The estate_property table stores real estate property details and metadata for transaction management.'
    _rec_name="property_name"

    active = fields.Boolean(default=True)
    property_name = fields.Char(required=True)

    partner_id= fields.Many2one("estate.customer", string="Partner")
    salseperson_id= fields.Many2one("estate.salesperson", string="Salesperson")
    property_type_id = fields.Many2many("estate.property.type", string="Property Type")
    offers_id= fields.One2many(comodel_name="estate.property.offers", inverse_name="property_id", string="Offers")

    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postal Code")
    date_availability = fields.Date("Availability Date", copy=False, default= fields.Date.add(fields.Date.today(), months=3))
    expected_price = fields.Float(string="Expected Price",required=True, digits=(8,2))
    selling_price = fields.Float(string="Selling Price",digits=(8,2), readonly=True, copy=False)
    bedrooms = fields.Integer(string="Bedrooms",default=2)
    living_area = fields.Integer(string="Living Area (feet²)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string="Garden Area (feet²)")
    total_area = fields.Integer(string="Total Area (feet²)", compute="_compute_totalarea")

    garden_orientation = fields.Selection(selection=[
        ('north', 'North'),
        ('south', 'South'),
        ('west', 'West'),
        ('east', 'East')
    ], string="Garden Orientation")

    property_state = fields.Selection(selection=[
         ('new','New'),
         ('offer received','Offer Received'),
         ('offer accepted','Offer Accepted'),
         ('sold','Sold'),
         ('cancelled','Cancelled')
    ],
    string= "State",
    copy=False,
    default="new",)

    @api.depends("garden_area", "living_area")
    def _compute_totalarea(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area
    
    @api.onchange("garden")
    def _onchange_garden(self):
        for record in self:
            if record.garden:
                record.garden_area = 10
                record.garden_orientation = 'north'
