# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from dateutil.relativedelta import relativedelta

from odoo import fields, models


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"

    name = fields.Char('Title', required=True)
    description = fields.Text("Description")
    postcode = fields.Char("Postcode")
    date_availability = fields.Date("Available From", copy=False, default=lambda self: fields.Date.context_today(self) + relativedelta(months=3))
    expected_price = fields.Float("Expected Price", required=True)
    selling_price = fields.Float("Selling Price", copy=False, readonly=True)
    bedrooms = fields.Integer("Bedrooms", default=2)
    living_area = fields.Integer("Living Area (sqm)")
    facades = fields.Integer("Facades")
    garage = fields.Boolean("Garage")
    garden = fields.Boolean("Garden")
    garden_area = fields.Integer("Garden Area (sqm)")
    garden_orientation = fields.Selection(
        selection = [
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')
        ],
        string="Garden Orientation"
    )

    active = fields.Boolean("Active", default=True)
    state = fields.Selection(
        selection = [
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled")
        ],
        string="Status", required=True, default="new", copy=False
    )

    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    user_id = fields.Many2one("res.users", string="Salesperson", default=lambda self: self.env.user)
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
