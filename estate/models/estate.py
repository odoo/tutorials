# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class Estate(models.Model):
    _name = "estate_property"
    _description = "RE Initial Model"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Date()
    date_availability = fields.Date()
    expected_price = fields.Float(required=True)
    selling_price = fields.Float()
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(string = 'Type', selection =[('north','North'),
                                                                       ('south', 'South'),
                                                                         ('east','East'),
                                                                            ('west','West')])
 