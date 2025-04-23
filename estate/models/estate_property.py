# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from typing_extensions import Required
from odoo import fields, models


class EstateProperty(models.Model):
    _name = "estate_property"
    _description = "Estate property"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date()
    expected_price = fields.Float(required=True)
    selling_price = fields.Float()
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation =fields.Selection(
        string='Orientation',
        selection=[('north', 'North'), ('south', 'South'),
        ('east', 'East'), ('west', 'West')])
