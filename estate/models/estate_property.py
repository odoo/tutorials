# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate property"
    _explanation = "Represents a real estate property"
    _order = "sequence"

    title = fields.Char(required=True)
    description = fields.Text()
    # property_type = fields.Selection([('house', 'House'), ('apartment', 'Apartment')], required=True)
    postcode = fields.Char()
    # tags = 
    date_availability = fields.Date()
    expected_price = fields.Float(required=True)
    selling_price = fields.Float()
    bedrooms = fields.Integer()
    living_area = fields.Integer('Living Area (sqm)')
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')])
    sequence = fields.Integer(default=10)

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
