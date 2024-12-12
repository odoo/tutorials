# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields

class Property(models.Model):
    _name = "estate.property"
    _description = "Estate property details"

    name = fields.Char(string='Name of the property', required=True, default='Property Name')
    description = fields.Text(string='Description of the property')
    
    postcode = fields.Char(string='Postal code')
    
    date_availability = fields.Date(string='Availability date')
    expected_price = fields.Float(string='Expected price', required=True, default=0.0)
    selling_price = fields.Float(string='Selling Price')
    
    bedrooms = fields.Integer(string='Number of bedrooms')
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([('north', 'North'), ('south', 'South'),
                                            ('east', 'East'), ('west', 'West')])
    
