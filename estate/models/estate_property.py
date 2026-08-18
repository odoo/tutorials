
from dateutil.relativedelta import relativedelta

from odoo import fields, models


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate Property Model'

    DEFAULT_BEDROOM_COUNT = 2
    DEFAULT_AVAILABILITY_DATE = fields.Date.today() + relativedelta(months=3)

    name = fields.Char(required=True)
    description = fields.Text()
    active = fields.Boolean()
    date_availability = fields.Date(copy=False, default=DEFAULT_AVAILABILITY_DATE)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    state = fields.Selection(
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('canceled', 'Canceled'),
        ],
        default='new',
    )

    bedrooms = fields.Integer(default=DEFAULT_BEDROOM_COUNT)
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West'),
        ],
    )
    living_area = fields.Integer()
    postcode = fields.Char()

    property_type_id = fields.Many2one('estate.property.type', string='Property Type')
    salesperson_id = fields.Many2one('res.users', string='Salesman', default=lambda self: self.env.user)
    buyer_id = fields.Many2one('res.partner', string='Buyer')

    tag_ids = fields.Many2many('estate.property.tag', string='Tags')

    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers')
