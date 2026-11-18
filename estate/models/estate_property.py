from calendar import month
from datetime import timedelta
from email.policy import default

from odoo import fields, models


class EstateProperty(models.Model):
    _name= 'estate.property'
    _description = 'Estate Property'

    name = fields.Char('Property Name', required=True, default="Unknown")
    description = fields.Text('Description')
    buyer_id = fields.Many2one('res.partner', string='Buyer', copy=False)
    salesperson_id = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.user)
    postcode = fields.Char('Postcode')
    date_availability = fields.Date('Available From', default=lambda self: fields.Date.context_today(
        self,
        timestamp=fields.Datetime.now() + timedelta(0,0,0,0,0,0,3*4)),
        copy=False)
    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float('Selling Price', readonly=True, copy=False)
    bedrooms = fields.Integer('Bedrooms', default=2)
    living_area = fields.Integer('Living Area')
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden Area')
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')]
    )
    active = fields.Boolean('Active', default=True)
    state = fields.Selection(
        string='Status',
        selection=[('new', 'New'),
                ('offer_received', 'Offer Received'),
                ('offer_accepted', 'Offer Accepted'),
                ('sold', 'Sold'),
                ('canceled', 'Canceled')],
        default='new'
    )
    last_seen = fields.Datetime('Last Seen', default=fields.Datetime.now)
    property_type_id = fields.Many2one('estate.property.type', string='Property Type')
    tag_ids = fields.Many2many('estate.property.tag', string='Tags')
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers')

