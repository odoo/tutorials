from typing import Required

from odoo import models, fields

class EstateProperty(models.Model):
    _name = 'estate_property'
    _description = "real estate property"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=lambda self:fields.Date.add(fields.Date.today(), months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(selection=[('north', 'North'),
                                                    ('east', 'East'),
                                                    ('west', 'West'),
                                                    ('south', 'South')])
    active = fields.Boolean(default=True)
    state = fields.Selection(selection=
                            [('new','New'),
                            ('offer received', 'Offer Received'),
                            ('offer accepted', 'Offer Accepted'),
                            ('sold','Sold'),
                            ('cancelled', 'Cancelled')],
                            required=True,
                            copy=False,
                            default='new')
    property_type_id = fields.Many2one("estate.property.type", string= "Property Type")
    buyer_id= fields.Many2one("res.partner", copy=False, string= "Buyer")
    salesperson_id = fields.Many2one("res.users", default=lambda self: self.env.user, string= "Salesperson")
    tag_ids= fields.Many2many("estate.property.tags")
    offer_id= fields.One2many("estate.property.offer", "property_id", string="Offers")
    