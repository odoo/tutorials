# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models
from datetime import timedelta


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate Property'

    name = fields.Char('Estate Property', required=True, default='Unknown', translate='True')
    active = fields.Boolean('Active', default=True)
    description = fields.Text('Description')
    postcode = fields.Char('Postcode')
    date_availability = fields.Date('Date Availability', copy=False, default=fields.Datetime.now() + timedelta(days=90))
    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float('Selling Price', readonly=True, copy=False)
    bedrooms = fields.Integer('Bedrooms', default=2)
    living_area = fields.Integer('Living Area')
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden Area')
    garden_orientation = fields.Selection(string='Garden orientation',
                                          selection=[('north', 'North'),
                                                    ('south', 'South'),
                                                    ('east', 'East'),
                                                    ('west', 'West')]
                                          )
    state = fields.Selection(string='State',
                            selection=[('new', 'New'),
                                    ('offer_received', 'Offer Received'),
                                    ('offer_accepted', 'Offer Accepted'),
                                    ('sold', 'Sold'),
                                    ('cancelled', 'Cancelled')],
                             default='new', required=True, copy=False)
