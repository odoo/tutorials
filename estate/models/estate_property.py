# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Properties"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date("Available From", default=fields.Date.add(fields.Date.today(), months = 3), copy=False)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(copy="False", readonly=True)
    bedrooms = fields.Integer(index=True, default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection=[
            ('north','North'),
            ('south','South'),
            ('east','East'),
            ('west','West'),
        ])
    active = fields.Boolean(default=True)
    state = fields.Selection(
        selection=[
            ('new','New'),
            ('offer received','Offer Received'),
            ('offer accepted','Offer Accepted'),
            ('sold','Sold'),
            ('cancelled','Cancelled'),
        ],
        copy=False,
        default='new'
    )
