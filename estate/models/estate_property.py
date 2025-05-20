from datetime import datetime, timedelta
from odoo import fields, models


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Property's properties"

    name = fields.Char('Property name', required=True, default='Unknown')
    description = fields.Text('Property description')
    postcode = fields.Char('Postcode')
    date_availability = fields.Date('Availability', copy=False, default=datetime.now() + timedelta(days=90))
    expected_price = fields.Float('Expected price', required=True)
    selling_price = fields.Float('Selling price', readonly=True, copy=False)
    bedrooms = fields.Integer('Bedrooms', default=2)
    living_area = fields.Integer('Living area')
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden Area')
    garden_orientation = fields.Selection([('North', 'North'), ('East', 'East'), ('South', 'South'), ('West', 'West')], default='North')
    active = fields.Boolean('Active', default=True)
    state = fields.Selection([
        ('New', 'New'), ('Offer received', 'Offer received'), ('Offer accepted', 'Offer accepted'), ('Sold', 'Sold'), ('Cancelled', 'Cancelled')
    ], default='New', required=True, copy=False)
