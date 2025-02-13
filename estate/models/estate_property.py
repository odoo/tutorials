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
    price = fields.Float(string="Price")
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
    
    # Compute Total Area which is depend on living_are and gardern_area
    total_area=fields.Float(string="Total Area (sqm)", compute="_compute_total")
    api.depends("living_area","garden_area")
    def _compute_total(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    best_price=fields.Float(string="Best Price",compute="_compute_best_price")
    api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.best_price=max(record.mapped("offer_ids.price"),default=0)
    partner_id=fields.Many2many("res.partner",string="owner")