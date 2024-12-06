
from odoo import fields, models


class RecurringPlan(models.Model):
    _name = "estate.property"
    _description = "Estate Property Table"

    name = fields.Char('Name', required=True)
    description = fields.Text('Description', required=True)
    postcode = fields.Char('PostCode', required=True)
    date_availability= fields.Date('Availability Date', required=True,copy=False)
    selling_price = fields.Float('Selling Price',readonly=True,copy=False)
    expected_price = fields.Float('Expected Price', required=True)
    bedrooms = fields.Integer('Bedrooms', required=True,default=2)
    living_area = fields.Integer('Living Area', required=True)
    facades = fields.Integer('Facades', required=True)
    garage = fields.Boolean('Garage', required=True)
    garden = fields.Boolean('Garden', required=True)
    garden_area = fields.Integer('Garden Area', required=True)
    garden_orientation = fields.Selection([('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')], 'Garden Orientation', required=True)
    state = fields.Selection([('new', 'New'), ('offer received', 'Offer Received'), ('offer accepted', 'Offer Accepted'), ('sold', 'Sold'), ('cancelled', 'Cancelled')], required=True, default='new')
    active = fields.Boolean('Active', required=True, default=False)
