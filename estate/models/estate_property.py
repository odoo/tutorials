# -*- coding: utf-8 -*-
from datetime import timedelta
from odoo import fields, models

class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Property'
    _order = 'name'


    name = fields.Char("Property", required=True)
    description = fields.Text("Description")
    
    active = fields.Boolean(string="Active", default=True, required=True)
    state = fields.Selection(
        string="State",
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

    date_availability = fields.Date(
        string="Available From",
        default=(lambda _: fields.Date.today() + timedelta(days=90)),
        copy=False,
    )

    # Price fields:
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        string="Currency",
    )
    expected_price = fields.Monetary(
        string="Expected Price",
        required=True,
    )
    selling_price = fields.Monetary(
        string="Selling Price",
    )

    # Address fields:
    street = fields.Char("Street")
    street2 = fields.Char("Street (line 2)")
    city = fields.Char("City")
    postcode = fields.Char("Postcode")
    state_id = fields.Many2one(
        comodel_name="res.country.state",
        string='State',
        domain="[('country_id', '=?', country_id)]",
    )
    country_id = fields.Many2one(
        comodel_name='res.country',
        string='Country',
    )

    # Amenity fields:
    bedrooms = fields.Integer(string="Bedrooms", default=2, help="Number of bedrooms")
    living_area = fields.Integer(string="Living Area (sqm)", help="Habitable area of the property (m^2)")
    facades = fields.Integer(string="Facades", help="Number of facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area (sqm)", help="Size of the garden (m^2)")
    garden_orientation = fields.Selection(
        string='Garden orientation',
        selection=[
            ('n', 'North'),
            ('s', 'South'),
            ('e', 'East'),
            ('w', 'West'),
        ],
        help="Direction the garden faces",
    )
