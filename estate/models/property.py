from odoo import fields, models, api
from datetime import timedelta

class Property(models.Model):
    _name = 'estate.property'
    _description = 'Real Estate Property'

    name = fields.Char('name', required=True, translate=True)
    description = fields.Text('description')
    postcode = fields.Char('postcode', required=True)
    date_available = fields.Date('date_available', required=True, copy=False, default=fields.Date.today() + timedelta(days=30))
    expected_price = fields.Float('expected_price', required=True)
    selling_price = fields.Float('selling_price', readonly=True, copy=False)
    bedrooms = fields.Integer('bedrooms', required=True, default=2)
    living_area = fields.Integer('living_area', required=True)
    facades = fields.Integer('facades', required=True)
    garage = fields.Boolean('garage', required=True)
    garden = fields.Boolean('garden', required=True)
    garden_area = fields.Integer('garden_area')
    garden_orientation = fields.Selection(
        string='garden_orientation',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        help='Direction the garden is facing')
    active = fields.Boolean('active', default=False)
    state = fields.Selection(
        string='state',
        selection=[('new', 'New'), ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'), ('canceled', 'Canceled')],
        default='new'
    )

    # _sql_constraints = [
    #     ('check_number_of_months', 'CHECK(number_of_months >= 0)', 'The number of month can\'t be negative.'),
