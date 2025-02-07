from datetime import timedelta

from odoo import models, fields


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate property'

    name = fields.Char(string="Name", required=True, default='Unknown')
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode",size=6)
    date_availability = fields.Date(string='Available From', default=(fields.Date.today() + timedelta(days=90)).strftime('%Y-%m-%d'), copy=False)
    expected_price = fields.Float(string="Expected Price")
    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string='Living Area (sqm)')
    facades = fields.Integer(string="Name")
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')
            ]
        )
    state = fields.Selection(
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled')
            ],
            default='new'
        )
    active = fields.Boolean(default=True)
    property_type_id = fields.Many2one(comodel_name="estate.property.type",string="Property Type")
    salesman_id = fields.Many2one(comodel_name='res.users', string='Salesman', default=lambda self: self.env.user)
    buyer_id = fields.Many2one(comodel_name='res.partner', string='Buyer', copy=False)
    tag_ids = fields.Many2many(comodel_name='estate.property.tag',string='Tags')
    offer_ids = fields.One2many(comodel_name='estate.property.offer', inverse_name='property_id', string='Offer')
