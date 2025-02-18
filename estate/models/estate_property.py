# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models
from dateutil.relativedelta import relativedelta


class Property(models.Model):
    _name = "estate.property"
    _description = "Real Estate Properties"
    
    property_type_id = fields.Many2one('estate.property.type', string='Property Type')
    property_tag_ids = fields.Many2many('estate.property.tag', string='Property Tags')
    property_offer_ids = fields.One2many('estate.property.offer', 'property_id')
    
    name = fields.Char('Title', required=True, translate=True, default="Best House In Town")
    active = fields.Boolean('Active', default=True)
    description = fields.Text('Description', default="Yo yo yo, no dup for date and status !")
    postcode = fields.Char('Postcode', translate=True)
    date_availability = fields.Date('Available From', copy=False, default=lambda self: fields.Date.today() + relativedelta(months=3))
    expected_price = fields.Float('Expected price', required=True)
    selling_price = fields.Float('Selling Price', readonly=True, copy=False)
    bedrooms = fields.Integer('Bedrooms', default=2)
    living_area = fields.Integer('Living Area (sqm)')
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Garage', default=False)
    garden = fields.Boolean('Garden', default=False)
    garden_area = fields.Integer('Garden Area (sqm)')
    garden_orientation = fields.Selection(
        string='Garden Orientation', 
        selection = [('north', "North"), ('south', 'South'), ('east', 'East'), ('west', 'West')]
    )
    state = fields.Selection(
        string='State', 
        selection = [('new', "new"), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'), ('cancelled', 'Cancelled')],
        default='new'
    )