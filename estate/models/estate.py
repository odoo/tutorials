# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models
from datetime import datetime, timedelta
from dateutil.relativedelta import *


class Estate(models.Model):
    _name = "estate_property"
    _description = "RE Initial Model"
    name = fields.Char(required=True)
    active = fields.Boolean(default = True)
    description = fields.Text()
    postcode = fields.Text()
    date_availability = fields.Date(copy=False, default=fields.Date.today()+relativedelta(months=+3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(string='Graden Orientation', selection=[('north','North'),
                                                                       ('south', 'South'),
                                                                         ('east','East'),
                                                                            ('west','West')])
    
    state = fields.Selection(string='State', default='new', copy = False, selection=[('new','New'),
                                                                       ('offer received', 'Offer Received'),
                                                                         ('offer accepted','Offer Accepted'),
                                                                            ('sold','Sold'), ('cancelled','Cancelled')])
 
