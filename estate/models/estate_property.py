from odoo import models, fields


class EstateProperty(models.Model):

    # ..................private attribute..................
    _name = "estate.property"
    _description = "These are Estate Module Properties"

    # ..................fields attribute..................
    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description"
    
    )
    postcode = fields.Char(
        string="Postcode"
    )
    date_availability = fields.Date(
        string="Date Availability", 
        default=lambda self: fields.Date.add(fields.Date.today(), months=3)
    )
    expected_price = fields.Float(
        string="Expected Price", 
        required=True
    )
    selling_price = fields.Float(
        string="Selling Price"
    )
    bedrooms = fields.Integer(
        string="Bedrooms", 
        default=2
    )
    living_area = fields.Integer(
        string="Living Area"
    )
    facades = fields.Integer(
        string="Facades"
    )
    garage = fields.Boolean(
        string="Garage"
    )
    garden = fields.Boolean(
        string="Garden"
    )
    garden_area = fields.Integer(
        string="Garden Area"
    )
    garden_orientation = fields.Selection(
        selection=[
            ('n', 'North'),
            ('s', 'South'),
            ('e', 'East'),
            ('w', 'West')
        ],
        string="Garden Orientation"
    )
    state = fields.Selection(
        string="Status", 
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled')
        ],
        default='new',
        copy=False, 
        required=True
    )
    active = fields.Boolean(
        string="Active", 
        default=True
    )

    # estate_property_type_id = fields.Many2one(
    #     comodel_name="estate.property.type", 
    #     string="Property Type"
    # )
