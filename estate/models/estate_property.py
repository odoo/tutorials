from odoo import fields, models
from datetime import date
from dateutil.relativedelta import relativedelta

class EstatePropertyModel(models.Model):
    _name = "estate.property"
    _description = "Estate Property"


    title = fields.Char(required=True)
    active = fields.Boolean(default=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availablility = fields.Date(default=date.today() + relativedelta(months=3), copy=False)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([('EAST','East'),('WEST','West'), ('SOUTH','South'), ('NORTH','North')])
    state = fields.Selection([("NEW","New"), ("OFFER_RECEIVED","Offer Received"), ("OFFER_ACCEPTED","Offer Accepted"), ("SOLD","Sold"), ("CANCELLED","Cancelled")], required=True, copy=False, default="NEW")
    