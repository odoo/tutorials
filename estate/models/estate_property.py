from odoo import fields, models
import datetime
from dateutil.relativedelta import relativedelta

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "this is the estate property model"
    name = fields.Char('Name', required=True)
    description = fields.Text('Description')
    postcode = fields.Char('Postal Code')
    date_availability = fields.Date(default=datetime.date.today() + relativedelta(months=5), copy=False)
    expected_price = fields.Float(digits=(20, 2), required=True)
    selling_price = fields.Float(digits=(20, 2), readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(selection=[
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West')])
    state = fields.Selection(selection=[
        ('new', 'New'),
        ('offer', 'Offer'),
        ('received', 'Received'),
        ('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('cancelled', 'Cancelled')
    ], copy=False, required=True, default='new')
    active = fields.Boolean(default=True)
    _sql_constraints = []
