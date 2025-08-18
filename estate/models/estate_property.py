from odoo import models, fields
from datetime import timedelta

class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate Property'

    name = fields.Char(string="Name",required=True)
    description = fields.Text(string="Description")
    active = fields.Boolean(
        string="Active",
        default=True, 
        help="Mark as active if you want the property to be listed.",)
    postcode = fields.Char(string="Postcode")
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    date_availability = fields.Date(
        string='Available From',
        default= fields.Date.today() + timedelta(days=90), 
        copy=False)
    expected_price = fields.Float(string="Expected Price",required=True)
    selling_price = fields.Float(string="Selling Price" ,readonly=True ,copy=False)
    bedrooms = fields.Integer(string="Bedrooms",default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection = [
            ('north', 'North'), 
            ('south', 'South'), 
            ('east', 'East'), 
            ('west', 'West')
        ],
    )
    state = fields.Selection(
        string="State",
        required=True,
        default="new",
        copy=False,
        selection=[
            ("new", "New"),
            ("offer received", "Offer Received"),
            ("offer accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
    )
    salesman_id = fields.Many2one(
        "res.users", string="Salesman", default=lambda self: self.env.user
    )
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy = False) 

    tag_ids = fields.Many2many(
        'estate.property.tag', 
        string='Tags', 
        help='Properties associated with this tag.'
    ) 

    offer_ids = fields.One2many(
        'estate.property.offer',
        'property_id',
        string='Offers',
        help='Offers made on this property.')