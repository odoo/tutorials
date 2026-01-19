import datetime
from dateutil.relativedelta import relativedelta

from odoo import fields, models

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real estate property model"

    name = fields.Char(required=True, string="Title")
    description= fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=datetime.date.today() + relativedelta(months=3), string="Available From")
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West'),
        ]
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(required=True, default='new', copy=False,
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled")
        ],
    )
