from odoo import models, fields # type: ignore
from dateutil.relativedelta import relativedelta

class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate Property'

    name = fields.Char(string='Property Name', required=True)
    description = fields.Text(string='Description')
    postcode = fields.Char(string='Postcode')
    date_availability = fields.Date(string='Availability Date', default=fields.Date.today() + relativedelta(months=3), copy=False)
    expected_price = fields.Float(string='Expected Price', required=True)
    selling_price = fields.Float(string='Selling Price', readonly=True)
    bedrooms = fields.Integer(string='Bedrooms', default=1)
    living_area = fields.Float(string='Living Area (sqm)')
    facades = fields.Integer(string='Facades', default=0)
    garage = fields.Boolean(string='Garage', default=False)
    garden = fields.Boolean(string='Garden', default=False)
    garden_area = fields.Float(string='Garden Area (sqm)')
    garden_orientation = fields.Selection(
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')
        ],
        string='Garden Orientation'
    )
    state = fields.Selection(
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled')
    ])

    property_type_id = fields.Many2one(comodel_name='estate.property.type', string='Property Type')
    buyer_id = fields.Many2one(comodel_name='res.partner', string='Buyer')
    salesperson_id = fields.Many2one(comodel_name='res.users', string='Salesman', default=lambda self: self.env.user)

    tag_ids = fields.Many2many(comodel_name='estate.property.tag', string='Tags')

    offer_ids = fields.One2many(comodel_name='estate.property.offer', inverse_name='property_id', string='Offers')