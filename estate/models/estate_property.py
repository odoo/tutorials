from odoo import fields, models, api
from datetime import timedelta  

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"

    name = fields.Char(string="Property Name", required=True)
    active = fields.Boolean(string="Active", default=True)
    description = fields.Text()
    postcode = fields.Char(string="Postcode")

    # Setup the default availability date to 3 months from the current date
    date_availability = fields.Date(
        string="Availability Date", 
        copy=False, 
        default=lambda self: fields.Date.today() + timedelta(days=90)
    )

    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False)

    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer()

    # Boolean fields for garage and garden
    is_garage = fields.Boolean(string="Has Garage?")
    is_garden = fields.Boolean(string="Has Garden?")
    garden_area = fields.Integer(string="Garden (sqm)")

    # Selecting garden orientation from predefined options
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West')
    ], string="Garden Orientation")

    state = fields.Selection([
        ('new', 'New'),
        ('offer_received', 'Offer Received'),
        ('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('cancelled', 'Cancelled')
    ], string='State', default="new", copy=False)

    # Relations Between Models
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")

    salesperson_id = fields.Many2one(
        "res.users",
        string="Salesperson",
        default=lambda self: self.env.user
    )

    buyer_id = fields.Many2one(
        "res.partner",
        string="Buyer",
        copy=False
    )

    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers')
    
    @api.onchange('is_garden')
    def _onchange_is_garden(self):
        if not self.is_garden:
            self.garden_area = 0
