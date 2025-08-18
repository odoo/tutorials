from odoo import models, fields
from datetime import timedelta

class EstateModel(models.Model):
    _name = "estate.property"
    _description = "Real Estate Advertisement Model"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        copy=False,
        default= fields.Date.today() + timedelta(days=90)
        )
    active= fields.Boolean(default=True)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    state= fields.Selection(
        string='state',
        default="New",
        required=True,
        copy=False,
        selection=[('New', 'New'),('Offer Received', 'Offer Received'),('Offer Accepted', 'Offer Accepted'),('Sold', 'Sold'), ('Cancelled', 'Cancelled'),
        ]
    )
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[('north', 'North'),('south', 'South'),('east', 'East'),('west', 'West'),
        ],
        help="Select the direction the garden faces"
    )