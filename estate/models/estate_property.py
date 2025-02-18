from odoo import fields, models
from datetime import timedelta



class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Model containing basic info of a property"

    name = fields.Char(required=True, default='Unknown')
    description = fields.Text('Notes')
    postcode = fields.Char()
    date_availability = fields.Date(default=fields.Date.today() + timedelta(days=90), copy=False)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    last_seen = fields.Datetime('Last Seen', default=fields.Datetime.now)
    garden = fields.Boolean()
    garden_area = fields.Integer()
    active=fields.Boolean('Active', default=True)
    garden_orientation = fields.Selection(
        string='Garden orientation',
        selection=[
            ('north', 'North'),
            ('east', 'East'),
            ('west', 'West'),
            ('south', 'South')
        ]
    )
    state = fields.Selection(
        string='State',
        required=True,
        copy=False,
        default='new',
        selection=[
            ('new', 'New'),
            ('offer received', 'Offer Received'),
            ('offer accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled')
        ]
    )
