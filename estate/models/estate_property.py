# -*- coding: utf-8 -*-
from odoo import models, fields


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Properties of the estate"

    name = fields.Char(required=True, string="Title")
    description = fields.Text()
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")

    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    salesperson_id = fields.Many2one("res.users", default=lambda self: self.env.user)
    buyer_id = fields.Many2one("res.partner", copy=False)
    offer_ids = fields.One2many("estate.property.offer", "property_id", copy=False)

    postcode = fields.Char()
    date_availability = fields.Date(copy=False, string="Available From", default=lambda self: fields.Date.add(fields.Date.today(), months=3))
    expected_price = fields.Float(required=True, string="Expected Price")
    selling_price = fields.Float(readonly=True, string="Selling Price", copy=False)

    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facade = fields.Integer(string="Façade")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[("north", "North"), ("south", "South"), ("east", "East"), ("west", "West")],
    )
    
    active = fields.Boolean(default=True)
    state = fields.Selection(
        string="Status",
        selection=[("new","New"), ("offer_received","Offer Received"), ("offer_accepted","Offer Accepted"), ("sold","Sold"), ("canceled","Canceled")],
        required=True,
        copy=False,
        default="new"
    )


