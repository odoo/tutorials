from datetime import date
from dateutil.relativedelta import relativedelta

from odoo import models,fields


class EstateProperty(models.Model):
    _name = "estate.property"  # . will be shown as _ in actual database 
    _description = "listing for the properties"

    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Post Code", index=True)

    date_availability = fields.Date(
        string="Date Availability",
        default=lambda self:date.today()+relativedelta(months=3),
        copy=False
    )
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area")

    facades = fields.Integer(
        string="Facades",
        help="A facade in real estate is the exterior wall of a building, usually the front face."
    )

    garage = fields.Boolean(string="Garage?")
    garden = fields.Boolean(string="Garden?")
    garden_area = fields.Integer(string="Garden Area")
    garden_orientation = fields.Selection(
        selection=[
            ('north','North'),
            ('south','South'),
            ('east','East'),
            ('west','West')
        ])

    active = fields.Boolean(string="Active", default=True)
    state = fields.Selection(
        string='Status',
        selection=[
            ('new','New'),
            ('offer_received','Offer Received'),
            ('offer_accepted','Offer Accepted'),
            ('sold','Sold'),
            ('cancelled','Cancelled')
        ],
        required=True,
        copy=False,
        default='new'
    )
    property_type_id = fields.Many2one('estate.property.type', string='Property Type')
    salesperson = fields.Many2one('res.users',string='Salesman', default=lambda self:self.env.user)
    buyer = fields.Many2one('res.users',string='Buyer', copy=False)
    tag_ids = fields.Many2many('estate.property.tag', string='Tags')
    offer_ids = fields.One2many(comodel_name='estate.property.offer', inverse_name='property_id', string="Offers")
