# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models

class Property(models.Model):
    _name = "estate.property"
    _description = "Estate property model"

    name = fields.Char('Property Name', required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date('Date of Availability',copy=False)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True,copy=False)
    bedrooms = fields.Integer('No. of Bedrooms',default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    active = fields.Boolean(default=True)
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection = [('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')]
    ),
    state = fields.Selection(
        [("new", "New"), ("offer_received", "Offer Received"), ("offer_accepted", "Offer Accepted"), ("sold", "Sold"), ("cancelled", "Cancelled")],
        required=True, default="new", copy=False)
