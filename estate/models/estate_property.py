from odoo import models, fields

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "estate property description"

    name = fields.Char('Name', required=True)
    description = fields.Text('Description')
    postcode = fields.Char('Postcode')
    date_availability = fields.Date('Date Availability', copy=False)
    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float('Selling Price', readonly=True, copy=False)
    bedrooms = fields.Integer('Bedrooms', default=2)
    living_area = fields.Integer('living_area')
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden Area')
    garden_orientation = fields.Selection( string='Garden Orientation',
        selection=[
            ('north', 'North'),
            ('south', "South"),
            ('east', 'East'),
            ('west', 'West'),
            ]
    )
    active = fields.Boolean(default=False)
    state = fields.Selection( string='State', required=True, copy=False, default='new',
        selection=[
            ('new', 'New'),
            ('offer Received', 'Offer Received'),
            ('offer Accepted', 'Offer Received'),
            ('sold', 'Sold'),
            ('canceled', 'Canceled')
        ]        
    )
