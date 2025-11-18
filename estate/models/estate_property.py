import datetime as dt

from odoo import fields, models


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "An awesome estate module"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=dt.datetime.today() + dt.timedelta(days=90))
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
        selection=[('north', 'North'), ('west', 'West'), ('south', 'South'), ('east', 'East')],
        help="Choose the appropriate orientation of the garden"
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        string="Estate status",
        selection=[('new', 'New'), ('offer received', 'Offer Received'), ('offer accepted', 'Offer Accepted'), ('sold', 'Sold'), ('cancelled', 'Cancelled')],
        help='This field explain the estate status.',
        required=True,
        copy=False,
        default='new'
    )
