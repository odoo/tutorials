from odoo import models, fields


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "real estate property"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=fields.Date.add(fields.Date.today(), months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string='orientation',
        selection=[('north', 'North'),
                   ('south', 'South'),
                   ('east', 'East'),
                   ('west', 'West')],
        help="Orientation is used to determine garden orientation"
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        string='state',
        selection=[('new', 'New'),
                   ('offer received', 'Offer Received'),
                   ('offer accepted', 'Offer Accepted'),
                   ('sold', 'Sold'),
                   ('canceled', 'Candeled')],
        required=True,
        copy=False,
        default="new",
        help="State is the current offer status of the property"
    )
