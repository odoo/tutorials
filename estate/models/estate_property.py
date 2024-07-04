from odoo import fields, models
from datetime import date, timedelta

default_availability_date = (date.today() + timedelta(days=90)).strftime("%Y-%m-%d")


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate properties defined"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=default_availability_date)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')])
    state = fields.Selection(selection=[('new', 'New'), ('offer received', 'Offer Received'), ('offer accepted', 'Offer Accepted'), ('sold and canceled', 'Sold and Canceled')], required=True, copy=False, default='new')
    active = fields.Boolean(string="Active", default=False)
