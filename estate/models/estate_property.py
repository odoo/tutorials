from dateutil.relativedelta import relativedelta
from odoo import fields, models


class Estate(models.Model):
    _name = 'estate.property'
    _description = 'It allows to manage your properties'

    name = fields.Char(required=True, default='Unknown')
    property_type_id = fields.Many2one('estate.property.type')
    last_seen = fields.Datetime('Last Seen', default=fields.Datetime.now)
    description = fields.Char(required=True)
    postcode = fields.Char()
    date_availability = fields.Date(
        default=fields.Date.today() + relativedelta(months=3), copy=False
    )
    active = fields.Boolean(default=True)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string='Orientation',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
    )
    state = fields.Selection(
        string='State',
        selection=[
            ('new', 'New'),
            ('offer received', 'Offer Received'),
            ('offer accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled'),
        ],
        default='new',
        readonly=True,
    )
