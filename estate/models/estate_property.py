from datetime import date, timedelta
from pickle import FALSE, TRUE
from odoo import models, fields

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(default=lambda self:date.today()+timedelta(days=90),copy=False)
    active= fields.Selection([('new','New'),('offer_received','Offer Received'), ('offer_accepted','Offer Accepted'),('sale','Sold')])
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=TRUE, copy=FALSE)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West'),
    ])
