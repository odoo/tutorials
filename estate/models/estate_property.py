# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    #_order = "sequence"
    
    name = fields.Char(string='Title', required=True)
    description = fields.Text(string='Description')
    postcode = fields.Char(string='Postcode')
    date_availability = fields.Date(string='Date Availability', copy=False, default=fields.Datetime.add(fields.Datetime.today(), months = 3))
    expected_price = fields.Float(string='Expected Price', required= True)
    selling_price = fields.Float(string='Selling Price', copy=False, readonly=True)
    bedrooms = fields.Integer(string='Bedrooms', default=2)
    living_area = fields.Integer(string='Living Area (sqm)')
    facades = fields.Integer(string='Facades')
    garage = fields.Boolean(string='Garage')
    garden = fields.Boolean(string='Garden')
    garden_area = fields.Integer(string='Garden Area (sqm)')
    garden_orientation = fields.Selection(selection=[('north', 'North'),('east','East'),('south','South'),('west','West')],string='Garden Orientation')
    active = fields.Boolean(string="Active", default=True)
    state = fields.Selection(selection=[('new', 'New'),('offerReceived', 'Offer Received'), ('offerAccepted', 'Offer Accepted'), ('sold', 'Sold'), ('canceled', 'Canceled')], default='new', copy=False, string='Status')

    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer")
    salesperson_id = fields.Many2one("res.users", string="Salesperson")
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer","property_id" ,string="Offers")