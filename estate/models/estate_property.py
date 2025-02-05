from datetime import datetime, timedelta
from odoo import fields, models

class estateModel(models.Model):
    _name = "estate.property"
    _description = "Estate testing model"

    id = fields.Integer()
    name = fields.Char('Estate Name', required=True)
    description = fields.Text('Description')
    postcode = fields.Char('Postcode')
    date_availability = fields.Date('Available From', copy=False, default=fields.Date.today() + timedelta(days=90))
    expected_price = fields.Float('Expected Price', default=2, required=True)
    selling_price = fields.Float('Selling Price', readonly=True)
    bedrooms = fields.Integer('Bedrooms')
    living_area = fields.Integer('Living Area')
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Is Garage')
    garden = fields.Boolean('Is garden')
    garden_area = fields.Integer('Garden Area')
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West')
    ], string='Garden Orientation')
    active = fields.Boolean(default=False)
    state = fields.Selection([
        ('new', 'New'),
        ('offer_received', 'Offer Received'),
        ('offer_accepted', 'Offer Accepted'),
        ('sold_and_cancelled', 'Sold and Cancelled'),
    ], string='Select State', required=True, copy=False, default='new')
