from odoo import fields, models
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
    living_area = fields.Integer("Living Area (m²)")
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
    
    # Relations
    property_type_id = fields.Many2one('estate.property.type', string="Property Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    salesperson_id = fields.Many2one("res.users", string="Salesperson", default=lambda self: self.env.user)
    tag_ids = fields.Many2many("estate.property.tag", string="Property Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
