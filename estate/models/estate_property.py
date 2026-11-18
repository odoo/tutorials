# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate property"
    _explanation = "Represents a real estate property"
    _order = "sequence"

    title = fields.Char('Title', required=True)
    description = fields.Text('Description')
    # property_type = fields.Selection([('house', 'House'), ('apartment', 'Apartment')], required=True)
    postcode = fields.Char('Postcode')
    # tags = 
    date_availability = fields.Date('Data availability')
    # expected_price = fields.Monetary('Expected Price')
    # selling_price = fields.Monetary('Selling Price')
    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float('Selling Price')
    bedrooms = fields.Integer('Bedrooms')
    living_area = fields.Integer('Living Area (sqm)')
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden area')
    garden_orientation = fields.Selection([('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')])
    sequence = fields.Integer('Sequence', default=10)

    _check_bedrooms = models.Constraint(
        'CHECK(bedrooms >= 0)',
        "The number of bedrooms can't be negative.",
    )

    _check_living_area = models.Constraint(
        'CHECK(living_area >= 0)',
        "The living area can't be negative.",
    )

    _check_facades = models.Constraint(
        'CHECK(facades >= 0)',
        "The number of facades can't be negative.",
    )

    _check_garden_area = models.Constraint(
        'CHECK(garden_area >= 0)',
        "The garden area can't be negative.",
    )
