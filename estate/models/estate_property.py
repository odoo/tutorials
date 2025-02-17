# -*- coding: utf-8 -*-

from odoo import fields, models


class Property(models.Model):
    _name = "estate.property"
    _description = "Real estate property"

    name = fields.Char("Property Name", required=True)
    description = fields.Text("Property description")
    postcode = fields.Char("Property postcode", required=True)
    date_availability = fields.Date("Property availability date")
    expected_price = fields.Float("Property expected price", required=True)
    selling_price = fields.Float("Property selling price")
    bedrooms = fields.Integer("Number of bedrooms", required=True)
    living_area = fields.Integer("Size of the living area", required=True)
    facades = fields.Integer("Number of facades", required=True)
    garage = fields.Boolean("Has a garage", required=True)
    garden = fields.Boolean("Has a garden", required=True)
    garden_area = fields.Integer("Size of the garden")
    garden_orientation = fields.Selection(
        string="Garden orientation",
        selection=[
            ("north", "North"),
            ("west", "West"),
            ("east", "East"),
            ("south", "South"),
        ],
    )
