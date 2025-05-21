from odoo import fields, models
from dateutil.relativedelta import relativedelta


class Property(models.Model):
    _name = "estate.property"
    _description = "Estate Properties"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(default=fields.Date.today() + relativedelta(months=3), copy=False)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    active = fields.Boolean(default=True)
    state = fields.Selection(
        string='Status',
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer received'),
            ('offer_accepted', 'Offer accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled')
        ],
        required=True,
        copy=False,
        default='new'
    )
    garden_orientation = fields.Selection(
            string='Type',
            selection=[
                ('north', 'North'),
                ('south', 'South'),
                ('east', 'East'),
                ('west', 'West')
            ],
            help="This is Garden orientation described in directions"
    )
