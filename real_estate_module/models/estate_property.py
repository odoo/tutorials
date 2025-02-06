from odoo import api, models, fields

class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Real Estate Property'

    name = fields.Char(
        string="Name",
        required=True,
        help="Name of the property, e.g., Bhat House"
    )
    
    postcode = fields.Char(
        string="Postcode",
        help="Postal code of the property"
    )
    
    description = fields.Text(
        string="Description",
        help="Detailed description of the property"
    )
    
    date_availability = fields.Date(
        string="Available Date",
        copy=False,
        default=fields.Date.today,
        help="Date when the property will be available for sale"
    )
    
    expected_price = fields.Float(
        string="Expected Price",
        required=True,
        help="Price at which the property is expected to be sold",
        index="btree"
    )
    
    selling_price = fields.Float(
        string="Selling Price",
        readonly=True,
        copy=False,
        help="The price at which the property is actually sold"
    )
    
    bedrooms = fields.Integer(
        string="No of Bedrooms",
        default=2,
        help="Number of bedrooms in the property"
    )
    
    living_area = fields.Integer(
        string="Living Area",
        help="The total living area of the property in square meters"
    )
    
    facades = fields.Integer(
        string="Facades",
        help="Number of facades of the property"
    )
    
    garage = fields.Boolean(
        string="Garage?",
        help="Indicates whether the property has a garage"
    )
    
    garden = fields.Boolean(
        string="Garden?",
        help="Indicates whether the property has a garden"
    )
    
    garden_area = fields.Integer(
        string="Garden Area",
        help="The area of the garden in square meters"
    )
    
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')
        ],
        help="The orientation of the garden"
    )
    
    active = fields.Boolean(
        string="Active",
        default=True,
        help="Indicates whether the property is active and available for sale"
    )
    
    state = fields.Selection(
        string="Current State",
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled')
        ],
        required=True,
        copy=False,
        default='new',
        help="The current state of the property"
    )
    
    property_type_id = fields.Many2one(
        "estate.property.type",
        string="Property Type",
        help="The type of the property (e.g., apartment, house, etc.)"
    )
    
    buyer = fields.Many2one(
        "res.partner",
        string="Buyer",
        help="The buyer who purchased the property"
    )
    
    salesman = fields.Many2one(
        "res.users",
        string="Salesman",
        default=lambda self: self.env.user,
        help="The salesperson responsible for the property"
    )
    
    tag_ids = fields.Many2many(
        "estate.property.tags",
        string="Tags",
        required=True,
        help="Tags associated with the property (e.g., luxury, beachfront)"
    )
    
    offer_ids = fields.One2many(
        "estate.property.offer",
        "property_id",
        help="Offers made for this property"
    )
    
    total_area = fields.Float(
        compute="_compute_total_area",
        help="The total area of the property (living area + garden area)"
    )
    
    best_price = fields.Float(
        compute="_compute_best_price",
        help="The best price offered for the property"
    )
    
    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area
    
    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped('price'))
            else:
                record.best_price = 0.0

    @api.onchange("garden")
    def _onchange_garden_area_orientation(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = ''
