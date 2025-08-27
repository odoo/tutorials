# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import datetime, timedelta
from odoo import models, fields


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate Property'

    name = fields.Char(string='Estate Property Name', required=True)
    description = fields.Text(string='Estate Property Description')
    postcode = fields.Char(string='Estate Property Postcode')
    date_availability = fields.Date(string='Estate Property Date Availability', copy=False, default=lambda self: datetime.now() + timedelta(days=90))
    expected_price = fields.Float(string='Expected Price Of Property', required=True)
    selling_price = fields.Float(string='Selling Price of Property', readonly=True, copy=False)
    bedrooms = fields.Integer(string='Number of Bedrooms in Property', default=2)
    living_area = fields.Integer(string='Number of Living Room in Property')
    facades = fields.Integer(string='Number of Facades in Property')
    garage = fields.Boolean(string='Property have garage or not')
    garden = fields.Boolean(string='Property have Garden or not')
    garden_area = fields.Integer(string='Number of Garden Area')
    garden_orientation = fields.Selection(
        string='Orientation of Garden',
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')
        ],
        help='Different Types of Directions')
    active = fields.Boolean(default=True)
    state = fields.Selection(
        string='State',
        default='new',
        copy=False,
        required=True,
        selection=[
            ('new', 'New'),
            ('offer_recieved', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold_and_cancelled', 'Sold and Cancelled')
        ],
        help='State of the property')
    property_type_id = fields.Many2one('estate.property.type', string='Property Type Id')
    buyer_id = fields.Many2one('res.users', string='Buyer', copy=False)
    salesman_id = fields.Many2one('res.partner', string='Salesman', default=lambda self: self.env.user)
    tag_ids = fields.Many2many('estate.property.tag', string='Estate property Tag')
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='offer')
