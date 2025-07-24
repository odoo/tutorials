from odoo import models, fields

class Property(models.Model):
    _name = 'estate.property'
    _description = 'Real Estate Property'

    name = fields.Char('Name', required=True)
    description = fields.Text('Description')
    active = fields.Boolean('Active', default=True)
    postcode = fields.Char('Postcode')
    date_availability = fields.Date('Date Availability', default=fields.Datetime.add(fields.Datetime.today(), month=3), copy=False)
    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float('Selling Price', readonly=True, copy=False)
    bedrooms = fields.Integer('Bedrooms', default=2)
    living_area = fields.Integer('Living Area')
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden Area')
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
    )
    state = fields.Selection(string='State', selection=[('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'), ('cancelled', 'Cancelled')], default='new')
