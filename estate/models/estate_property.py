# -*- coding: utf-8 -*-

from odoo import fields, models


class Property(models.Model):
    _name = "estate.property"
    _description = "Real estate property"

    name = fields.Char("Property Name", required=True)
    description = fields.Text("Property description")
    property_tag_ids = fields.Many2many("estate.property.tag", string="Tags")

    active = fields.Boolean(default=True)
    state = fields.Selection(
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        default="new",
        required=True,
        copy=False,
    )

    postcode = fields.Char("Property postcode", required=True)
    date_availability = fields.Date(
        "Property availability date",
        copy=False,
        default=fields.Datetime.add(fields.Datetime.today(), months=3),
    )
    expected_price = fields.Float("Property expected price", required=True)
    selling_price = fields.Float(
        "Property selling price", readonly=True, copy=False, default=0
    )
    bedrooms = fields.Integer("Number of bedrooms", required=True, default=2)
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
    property_type_id = fields.Many2one("estate.property.type", string="Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    salesperson_id = fields.Many2one(
        "res.users",
        string="Salesperson",
        default=lambda self: self.env.user,
    )
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
