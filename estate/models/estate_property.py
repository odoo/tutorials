# Part of Odoo. See LICENSE file for full copyright and licensing details.

from dateutil.relativedelta import relativedelta

from odoo import fields, models


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate property"
    _explanation = "Represents a real estate property"
    _order = "id desc"

    title = fields.Char(required=True)
    description = fields.Text()
    # property_type = fields.Selection([('house', 'House'), ('apartment', 'Apartment')], required=True)
    postcode = fields.Char()
    # tags =
    date_availability = fields.Date('Available From', default=fields.Date.today() + relativedelta(months=3), copy=False)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer('Living Area (sqm)')
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')])
    active = fields.Boolean(default=True)
    status = fields.Selection([
        ('new', 'New'),
        ('offer_received', 'Offer Received'),
        ('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('cancelled', 'Cancelled'),
    ],
        required=True,
        copy=False,
        default='new')

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
