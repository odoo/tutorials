# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models
from odoo.tools import relativedelta

class EstateProperty(models.Model):

    def _get_default_date_availability(self):
        return fields.Date.today() + relativedelta(months=3)

    _name = "estate.property"
    _description = "Real Estate Property"

    name = fields.Char(string="Title", required=True)
    description = fields.Text()
    active = fields.Boolean(default=True)
    state = fields.Selection([
        ('new', 'New'),
        ('offer_received', 'Offer Received'),
        ('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('canceled', 'Canceled')
    ], default='new', required=True, copy=False)

    tag_ids = fields.Many2many('estate.property.tag', string="Tags")
    property_type_id = fields.Many2one('estate.property.type', string="Property Type")
    salesman_id = fields.Many2one('res.users', string="Salesman", default=lambda self: self.env.user)
    buyer_id = fields.Many2one('res.partner', string="Buyer", copy=False)
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string="Offers")

    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(string="Available From", default=_get_default_date_availability, copy=False)
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False)

    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West')
    ])
