# -*- coding: utf-8 -*-
from dateutil.utils import today

from odoo.tools.date_utils import add

from odoo import fields, models


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate base property model"

    name = fields.Char(required=True)
    active = fields.Boolean(default=True)
    state = fields.Selection(
        selection=[("new", "New"), ("offer_received", "Offer Received"), ("offer_accepted", "Offer Accepted"),
                   ("sold", "Sold"), ("canceled", "Canceled")],
        default="new",
        required=True,
        copy=False
    )

    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=add(today(), months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection=[("north", "North"), ("south", "South"), ("east", "East"), ("west", "West")]
    )
