# -*- coding: utf-8 -*-

from odoo import fields, models


class EstateProperty(models.Model):
    _name = "estate_property"
    _description = "Estate property"

    name = fields.Char(string='Name of the Property',required=True)
    description = fields.Text(string='Description')
    postcode = fields.Char(string='Postcode')
    date_availability = fields.Date(string='Date of Availability')
    expected_price = fields.Float(string='Expected Selling Price',required=True)
    selling_price = fields.Float(string='Selling Price')
    bedrooms = fields.Integer(string='Number of Bedrooms')
    living_area = fields.Integer(string='Number of Living Areas')
    facades = fields.Integer(string='Number of Facades')
    garage = fields.Boolean(string='Has a garage')
    garden = fields.Boolean(string='Has a garden')
    garden_area = fields.Integer(string='Number of garden Areas')
    garden_orientation =fields.Selection(
        string='Orientation of the Garden',
        selection=[
            ('north', 'North'), 
            ('south', 'South'),
            ('east', 'East'), 
            ('west', 'West')
        ])