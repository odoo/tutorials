from odoo import fields, models

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West')
        ],
        help='Orientation of the garden')
    state = fields.Selection(
        string='Status',
        selection=[
        ('new', 'New'),
        ('offer_received', 'Offer Received'),
        ('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('cancelled', 'Cancelled')
        ],
        required=True,
        copy=False,
        default='new'
    )
    property_type_id = fields.Many2one('property.type', string='Property Type')
    tag_ids = fields.Many2many('property.tag', string='Property Tags')


