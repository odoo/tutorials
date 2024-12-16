# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields
from datetime import timedelta

class Property(models.Model):
    _name = "estate.property"
    _description = "Estate property details"

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    
    postcode = fields.Char(string='Postal code')
    
    date_availability = fields.Date(string='Availability Date', copy=False,
                                    default=fields.Date.today()+timedelta(days=90))

    expected_price = fields.Float(string='Expected Price', required=True, default=0.0)
    selling_price = fields.Float(string='Selling Price', readonly=True, copy=False)
    
    bedrooms = fields.Integer(string='Number of bedrooms', default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([('north', 'North'), ('south', 'South'),
                                            ('east', 'East'), ('west', 'West')])

    active = fields.Boolean(default=True)
    
    state = fields.Selection([('new', 'New'), ('offer received', 'Offer Received'),
                              ('offer accpeted', 'Offer Accepted'), ('cancelled', 'Cancelled')],
                               default="new",
                               required=True,
                               copy=False)
    
    property_type_id = fields.Many2one(
        'estate.property.type',
        string="Type",
        help="Select the category for this product"
    )

    property_seller_id = fields.Many2one(
        'res.users',
        string='Salesperson',
        default=lambda self: self.env.user
    ) 

    property_buyer_id = fields.Many2one(
        'res.partner',
        string='Buyer',
        copy=False
    )

    property_tag_ids = fields.Many2many(
        'estate.property.tag',
        copy=False
    )

    offer_ids = fields.One2many(
        comodel_name='estate.property.offer',
        inverse_name='property_id',
        string="Offers",
        copy=False
    )