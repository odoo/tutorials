# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class Estate(models.Model):
    _name = "estate"
    _description = "Table that contains estates data"
    _order = "sequence"

    name = fields.Char('Name', required=True, translate=True)
    description = fields.Text("Description", required=False)
    postcode = fields.Char('Postcode', required=False)
    date_availability = fields.Date('Date Availability', required=False)
    expected_price = fields.Float('Expected Price', required=False)
    selling_price = fields.Float('Selling Price', required=False)
    bedrooms = fields.Integer('Bedrooms', required=False)
    living_area = fields.Integer('Living Area', required=False)
    facades = fields.Integer('Facades', required=False)
    garage = fields.Boolean('Garage', required=False)
    garden = fields.Boolean('Garden', required=False)
    garden_area = fields.Integer('Garden Area', required=False)
    garden_orientation = fields.Selection(
        [('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        'Garden Orientation', required=False
    )
