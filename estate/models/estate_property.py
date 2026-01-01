from odoo import models, fields
from datetime import date, timedelta

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False,default=lambda self: fields.Date.today() + timedelta(days=90))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True,copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string='Direction', 
        selection=[('east', 'East'), ('west', 'West'), ('north', 'North'), ('south', 'South')],
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(string="state", selection=[('new','New'),('offer_received','Offer Received'),('offer_accepted','Offer Accepted'),('sold_and_cancelled','Sold and Cancelled')])
    
