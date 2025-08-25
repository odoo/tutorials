# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, fields


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"

    name = fields.Char(string='Estate Property Name', required=True)
    description = fields.Text(string='Estate Property Description')
    postcode = fields.Char(string='Estate Property Postcode')
    date_availability = fields.Date(string='Estate Property Date Availability')
    expected_price = fields.Float(string='Expected Price Of Property', required=True)
    selling_price = fields.Float(string='Selling Price of Property')
    bedrooms = fields.Integer(string='Number of Bedrooms in Property')
    living_area = fields.Integer(string='Number of Living Room in Property')
    facades = fields.Integer(string='Number of Facades in Property')
    garage = fields.Boolean(string='Property have garage or not')
    garden = fields.Boolean(string='Property have Garden or not')
    garden_area = fields.Integer(string='Number of Garden Area')
    garden_orientation = fields.Selection(
        string='Orientation of Garden',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        help="Different Types of Directions")
