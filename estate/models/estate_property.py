from dateutil.relativedelta import relativedelta

from odoo import fields, models

class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'There is the differents properties of the estate model'
    #_order = 'sequence'

    name = fields.Char('Title', required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        string='Available From',
        copy=False, 
        default=lambda self: fields.Date.context_today(self) + relativedelta(months=3)
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer('Living Area (m²)')
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer('Garden Area (m²)')
    garden_direction = fields.Selection(
        string='Garden Orientation',
        selection=[
            ('north', 'North'), 
            ('south', 'South'), 
            ('east', 'East'), 
            ('west', 'West')
        ]
    )
    active = fields.Boolean(default=True)
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
