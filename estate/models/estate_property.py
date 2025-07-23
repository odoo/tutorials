from odoo import models, fields

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=fields.Date.add(fields.Date.today(), months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(
        readonly=True,
        copy=False,
    )
    bedrooms = fields.Integer(default=2)
    living_area = fields.Float()
    facades = fields.Integer()
    garage = fields.Boolean(default=False)
    garden = fields.Boolean(default=False)
    garden_area = fields.Float()
    garden_orientation = fields.Selection(
        selection=[
            ('north', 'North'),
            ('east', 'East'),
            ('south', 'South'),
            ('west', 'West'),
        ],
        string="Garden Orientation",
        default='north',
    )
    state = fields.Selection(
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled'),
        ],
        default='new',
        string="Status",
        required=True,
        copy=False,
    )
    active = fields.Boolean(default=True)
