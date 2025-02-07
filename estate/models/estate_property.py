# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields
from datetime import datetime, timedelta


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Real Estate Property'

    property_type_id = fields.Many2one(
        "estate.property.type",
        string="Property Type"
    )
    buyer_id = fields.Many2one(
        "res.partner",
        string="Buyer",
        copy=False
    )
    salesperson_id = fields.Many2one(
        "res.users",
        string="Salesperson",
        default=lambda self: self.env.user,
        required=True
    )
    tag_ids = fields.Many2many(
        "estate.property.tag",
        string="Tags"
    )
    offer_ids = fields.One2many(
        "estate.property.offer",
        "property_id",
        string="Offers"
    )
    name = fields.Char(string="Property Name", required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(
        string="Availability Date",
        default=lambda self: fields.Date.to_string(datetime.today() + timedelta(days=90)),
        copy=False
    )
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')
        ],
        string="Garden Orientation"
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        selection=[
            ('new', 'New'),
            ('offer received', 'Offer Received'),
            ('offer accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled')
        ],
        string="State",
        required=True,
        copy=False,
        default='new'
    )
