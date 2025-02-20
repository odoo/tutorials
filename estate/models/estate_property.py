from odoo import models, fields
from datetime import datetime, timedelta


class Property(models.Model):
    _name = 'estate.property' 
    _description = 'estate property model'

    postcode = fields.Char(required=True)
    date_availability = fields.Date(required=True, 
                                    copy=False, 
                                    default=lambda self: (datetime.now() + timedelta(days=3*30)))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(required=True, default=0.0, copy=False)
    bedrooms = fields.Integer(required=True, default=2) 
    living_area = fields.Integer(required=True)
    facades = fields.Integer(required=True)
    garage = fields.Boolean(required=False)
    garden = fields.Boolean(required=False)
    garden_area = fields.Integer(required=True)
    garden_orientation = fields.Selection(
        selection=[
            ('north', 'North'), 
            ('south', 'South'), 
            ('east', 'East'), 
            ('west', 'West'),
        ],
        string='Garden Orientation',
        default='north',
    )
    name = fields.Char(default='Uknown')
    last_seen = fields.Datetime('Last seen', default=fields.Datetime.now)
    state = fields.Selection(
        selection=[
                ('New', 'new'),
                ('Offer Received', 'offer_received'),
                ('Offer Accepted', 'offer_accepted'),
                ('Sold', 'sold'),
                ('Cancelled', 'cancelled')],
        default="New",
        string="state",
    )
    active = fields.Boolean(default=True)
    description = fields.Text(default="when duplicated status and date are not copied")

    property_type_id = fields.Many2one('estate.property.type', string="Property Type")
    tag_ids = fields.Many2many('estate.property.tag', string="Property Tags")
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string="Offers")

    buyer_id = fields.Many2one('res.partner', string="Buyer", copy=False, default=None)
    salesperson_id = fields.Many2one('res.users', 
                                     string="Seller",
                                     default=lambda self: self.env.user)