# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models
from dateutil.relativedelta import relativedelta


class Property(models.Model):
    _name = "estate.property"
    _description = "Real Estate Properties"
    
    name = fields.Char('Name', required=True, translate=True)
    active = fields.Boolean('Active', default=True)
    description = fields.Text('Description')
    postcode = fields.Char('Postcode', translate=True)
    date_availability = fields.Date('Date availability', copy=False, default=lambda self: fields.Date.today() + relativedelta(months=3))
    expected_price = fields.Float('Expected price', required=True)
    selling_price = fields.Float('Selling price', readonly=True, copy=False)
    bedrooms = fields.Integer('# Bedrooms', default=2)
    living_area = fields.Integer('Living area')
    facades = fields.Integer('# Facades')
    garage = fields.Boolean('Garage', default=False, )
    garden = fields.Boolean('Garden', default=False)
    garden_area = fields.Integer('Garden area')
    garden_orientation = fields.Selection(
        string='Garden Orientation', 
        selection = [('north', "North"), ('south', 'South'), ('east', 'East'), ('west', 'West')]
    )
    state = fields.Selection(
        string='State', 
        selection = [('new', "new"), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'), ('cancelled', 'Cancelled')],
        default='new'
    )