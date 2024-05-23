from odoo import fields, models
from datetime import date, datetime, time
from dateutil.relativedelta import relativedelta


class EstateProperty(models.Model):
    _name = "estate_property"
    _description = "Estate property"
    name = fields.Char(required=True)

    description = fields.Text()

    postcode = fields.Char()

    date_availability = fields.Date(copy=False, default=fields.Date.add(fields.Date.today(), months=3))

    expected_price = fields.Float(required=True)

    selling_price = fields.Float(readonly=True)

    bedrooms = fields.Integer(default=2)

    living_area = fields.Integer()

    facades = fields.Integer()

    garage = fields.Boolean()

    garden = fields.Boolean()

    garden_area = fields.Integer()

    garden_orientation = fields.Selection(string='Orientation',
                                          selection=[('north', 'North'), ('south', 'South'), ('east', 'East'),
                                                     ('west', 'West')],
                                          help="help")
    active = fields.Boolean(default=True)
    state = fields.Selection(string='State',
                             selection=[('New', 'New'), ('Offer Received', 'Offer Received'),
                                        ('Offer Accepted', 'Offer Accepted'), ('Sold', 'Sold'),
                                        ('Canceled', 'Canceled')],
                             help="help", required=True, copy=False, default="New")
    property_type_id = fields.Many2one('estate_property_type', string='Property Type')
    salesman_id = fields.Many2one('res.users', string='Salesperson',
                                  default=lambda self: self.env.user)
    buyer_id = fields.Many2one('res.users', string='Buyer', copy=False)
    tag_ids = fields.Many2many("estate_property_tag", string='Tags')
    offer_ids = fields.One2many('offer',"property_id",string='Offer')
