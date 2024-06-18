# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import fields, models


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real estate property overview"

    name = fields.Char('Estate name', required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date('Aivailable from', copy=False, default=fields.Date.add(fields.Date.today(), months=3))

    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)

    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()

    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string='Orientation',
        selection=[('N', 'North'), ('E', 'East'), ('S', 'South'), ('W', 'West')],
        help="Orientation of the garden"
    )

    active = fields.Boolean(default=True)
    state = fields.Selection(
        string='Status',
        selection=[('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'), ('canceled', 'Canceled')],
        help='Availability status of the property',
        required=True, copy=False, default='new'
    )

    property_type = fields.Many2One("estate.property.type")
    salesman = fields.Many2One("res.partner")
    buyer = fields.Many2One("res.users")