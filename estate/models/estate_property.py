from odoo import models,fields
from datetime import date, timedelta

class Property(models.Model):
    _name = "estate.property"
    _description = "estate property details"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False,default=lambda self: fields.Date.today() + timedelta(days=90))
    expected_price =  fields.Float(required=True)
    selling_price = fields.Float(readonly=True,copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(selection=[('north','North'),('west','West'),('east','East'),('south','South')])
    active = fields.Boolean(default=False)
    state = fields.Selection(default='New',selection=[('New','New'),('Offer Received','Offer Received'),
    ('Offer Accepted','Offer Accepted'),('Sold','Sold'),('Cancelled','Cancelled')],copy=False,required=True)