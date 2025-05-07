from odoo import fields, models
from dateutil.relativedelta import relativedelta

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"

    # Basic Fields
    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    
    # Date Fields
    date_availability = fields.Date(
        string="Available From",
        copy=False,
        default=lambda self: fields.Date.today() + relativedelta(months=3)
    )
    
    # Price Fields
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False)
    
    # Property Details
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area (sqm)")
    
    # Selection Fields
    garden_orientation = fields.Selection(
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West'),
        ],
        string="Garden Orientation"
    )
    
    state = fields.Selection(
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled'),
        ],
        string="Status",
        required=True,
        copy=False,
        default='new'
    )
    
    active = fields.Boolean(string="Active", default=True)
    
    # Many2one, Many2many, One2many Relation to Property Type
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    
    salesperson_id = fields.Many2one(
    "res.users", 
    string="Salesperson", 
    default=lambda self: self.env.user
    )
    
    offer_ids = fields.One2many(
    "estate.property.offer",  
    "property_id",           
    string="Offers"
    )
    
    tag_ids = fields.Many2many("estate.property.tag", string="Tags", widget="many2many_tags" )
