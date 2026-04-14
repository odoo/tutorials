from odoo import fields, models
from odoo.tools import date_utils


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property for purchasing and selling properties"

    name = fields.Char(required=True, string="Property Name")
    description = fields.Char()
    postcode = fields.Char()
    date_availibility = fields.Date(copy=False, default=lambda self: fields.Date.today() + date_utils.get_timedelta(3, "month"))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West'),

        ],
    )
    state = fields.Selection(
        selection=[
            ('new', 'New'),
            ('offer received', 'Offer received'),
            ('offer accepted', 'Offer accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled')
        ],
    )
    property_type_id = fields.Many2one("estate.property.type", string="Property Type Id")
    tag_ids = fields.Many2many("estate.property.tag", string="Property Tags")
    salesperson = fields.Many2one('res.users', default=lambda self: self.env.user)
    buyer = fields.Many2one('res.partner', copy=False)
    offer_ids = fields.One2many('estate.property.offer', 'property_id')
    active = fields.Boolean()
