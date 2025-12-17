from odoo import fields, models


class Property(models.Model):
    _name = "estate.property"
    _description = "Real Estate property"

    name = fields.Char('Title', required=True, default='Unknown')
    active = fields.Boolean('Active', default=True)
    state = fields.Selection([
        ('new', 'New'),
        ('received offer', 'Received offer'),
        ('offer accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('cancelled', 'Cancelled'),
    ], string='State', required=True, copy=False, default='new')
    description = fields.Text('Description')
    last_seen = fields.Datetime("Last Seen", default=lambda self: fields.Datetime.now())
    postcode = fields.Char('Postcode')
    date_availability = fields.Date('Available from', copy=False, default=lambda self: fields.Date.add(fields.Date.today(), months=3))
    expected_price = fields.Float('Expected price', required=True)
    selling_price = fields.Float('Selling price', readonly=True, copy=False)
    bedrooms = fields.Integer('Bedrooms', default=2)
    living_area = fields.Integer('Living area (sqm)')
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden area (sqm)')
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West'),
    ], string='Garden Orientation')
