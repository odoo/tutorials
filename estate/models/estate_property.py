from datetime import date, timedelta

from dateutil.relativedelta import relativedelta

from odoo import fields, models


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate property"
    _order = ""

    name = fields.Char('Title', required=True)
    description = fields.Text('Description')
    postcode = fields.Char('Postcode')
    date_availability = fields.Date(
        'Available From',
        copy=False,
        default=lambda self: date.today() + relativedelta(months=3),
    )

    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float('Selling Price', readonly=True, copy=False)

    bedrooms = fields.Integer('Bedrooms', default=0)
    living_area = fields.Integer('Living Area (sqm)')
    facades = fields.Integer('Facades')

    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden Area (sqm)')
    garden_orientation = fields.Selection(
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West'),
        ],
        string='Garden Orientation',
    )

    active = fields.Boolean('Active', default=True)
