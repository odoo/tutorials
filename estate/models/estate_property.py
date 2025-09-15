from odoo import fields, models
from datetime import date, timedelta

class estate_property(models.Model):
    _name = "estate.property"
    _description = "estate thingie"

    name = fields.Char(required = True)
    description =  fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False,string="Available From", default=lambda self: date.today() + timedelta(days=90))
    expected_price = fields.Float(required = True)
    selling_price = fields.Float(readonly = True,copy=False)
    bedrooms = fields.Integer(default = 2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(selection = [('North', 'North'), ('South', 'South'),('East', 'East'),('West', 'West')])
    active = fields.Boolean(default = True)
    state = fields.Selection(required = True, default = 'New', copy = False, selection = [('New','New'),('Offer Received','Offer Received'),('Offer Accepted','Offer Accepted'),('Sold','Sold'),('Cancelled','Cancelled')])