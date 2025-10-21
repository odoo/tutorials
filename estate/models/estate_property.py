from odoo import fields, models
from datetime import date
from dateutil.relativedelta import relativedelta

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "property data"

    name = fields.Char('name', required=True)
    description = fields.Text('desc')
    postcode = fields.Char('postcode')
    date_availability = fields.Date(copy=False,default=date.today() + relativedelta(months=3))
    expected_price = fields.Float()
    selling_price = fields.Float(readonly=True,copy=False)
    bedrooms = fields.Integer('# Bedrooms', default=2)
    living_area = fields.Integer('living area size')
    facades = fields.Integer('# Facades')
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer('garden.size')
    garden_orientation = fields.Selection(
        string='Orientation',
        selection=[('North', 'North'), ('West', 'West'), ('East', 'East'), ('South', 'South')]
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        string='Sate',
        selection=[('New','New'), ('Offer Received','Offer Received'), ('Offer Accepted','Offer Accepted'), ('Sold','Sold'), ('Cancelled','Cancelled')],
        required=True,
        copy=False,
        default="New"
    )
