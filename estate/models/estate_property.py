from odoo import fields, models

from datetime import date
from dateutil.relativedelta import relativedelta

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate property"

    name = fields.Char("Title", required=True)
    description = fields.Text()
    postcode = fields.Char() 
    date_availability = fields.Date("Available From", default=(date.today() + relativedelta(months=+3)), copy=False)
    expected_price = fields.Float(required=True) 
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer("Living Area (sqm)") 
    facades = fields.Integer() 
    garage = fields.Boolean() 
    garden = fields.Boolean()
    garden_area = fields.Integer("Garden Area (sqm)") 
    garden_orientation = fields.Selection(
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')]
    )
    active = fields.Boolean('Active', default=True)
    state = fields.Selection(
        required=True,
        copy=False,
        default='new',
        selection=[('new', 'New'), ('offer received', 'Offer Received'), ('offer accepted', 'Offer Accepted'), ('sold', 'Sold'), ('canceled', 'Canceled'), ]
    )