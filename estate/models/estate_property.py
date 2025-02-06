from datetime import timedelta

from odoo import models, fields


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "test Property"

    name = fields.Char(required=True, default='Unknown')
    description = fields.Text()
    postcode = fields.Char(size=6)
    date_availability = fields.Date(string='Available From', default=(fields.Date.today() + timedelta(days=90)).strftime('%Y-%m-%d'), copy=False)
    expected_price = fields.Float()
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string='Living Area (sqm)')
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')
            ]
        )
    state = fields.Selection(
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled')
            ],
            default='new'
        )
    active = fields.Boolean(default=True)
