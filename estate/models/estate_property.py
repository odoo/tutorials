from odoo import fields, models
from datetime import datetime, timedelta

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Properties"
    

    name = fields.Char(required=True)
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    salesperson = fields.Many2one('res.users', string="Sales Person", default=lambda self: self.env.user)
    buyer = fields.Many2one('res.partner', string="buyer", copy=False)
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string="Offers")
    tag_ids = fields.Many2many("estate.property.tag", string="Tags ID")
    postcode = fields.Char()
    description = fields.Text()
    availability_date = fields.Date(default=lambda self: datetime.today() + timedelta(days=90), copy=False)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(default=10000, readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Float("Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Float("Garden Area (sqm)")
    garden_orientation = fields.Selection(
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')
        ],
        string="Garden Orientation"
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('canceled', 'Canceled')
        ],
        required=True,
        copy=False,
        default='new',
        string="Status",
    )

