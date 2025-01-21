from odoo import fields, models
from datetime import date
from dateutil.relativedelta import relativedelta

class TestModel(models.Model):
    _name = "estate_property"
    _description = "estate property description"

    name = fields.Char('Estate Name', required=True)

    property_type_id = fields.Many2one('estate_property_type', string='Property type')
    partner_id = fields.Many2one('res.partner', string='Buyer')
    users_id = fields.Many2one('res.users', string='Salesman', default=lambda self: self.env.user)

    active = fields.Boolean('Active', default=True)
    description = fields.Text('Description')
    postcode = fields.Char('Postcode')
    date_availability = fields.Date('Availability', copy=False, default=fields.Date.today() +  relativedelta(month=4))
    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float('Selling Price', readonly=True, copy=False)
    bedrooms = fields.Integer('Number of Bedrooms', default=2)
    living_area = fields.Integer('Number of Living Areas')
    facades = fields.Integer('Number of Facades')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden Area')
    garden_orientation = fields.Selection(
        selection=[
            ('north', 'North'), 
            ('south', 'South'), 
            ('east', 'East'), 
            ('west', 'West')])

    state = fields.Selection(
        selection=[
            ('new', 'New'), 
            ('offer received', 'Offer Received'), 
            ('offer accepted', 'Offer Accepted'), 
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled')], default="new", required=True, copy=False)