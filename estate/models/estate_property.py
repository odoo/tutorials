from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo import models, fields


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "This is a estate property app"

    def set_selection(self):
        
        return "north"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        default=fields.Date.today() + relativedelta(months=3), copy=False
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    is_garage = fields.Boolean("Garage")
    is_garden = fields.Boolean("Garden")
    garden_area = fields.Integer()
    property_type_id = fields.Many2one('estate.property.type', string='Property Type')
    salesman_id = fields.Many2one('res.users', default=lambda self: self.env.user)
    buyer_id = fields.Many2one('res.partner', copy=False)
    tag_ids = fields.Many2many('estate.property.tag', string='Tags')
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offer')
    garden_orientation = fields.Selection(
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
        default=set_selection,
    )
    active = fields.Boolean(default=True)
    status = fields.Selection(
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        default="new",
    )
