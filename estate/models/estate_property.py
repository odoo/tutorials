from datetime import timedelta

from odoo import fields, models


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"
    _order = "name"

    name = fields.Char('Property Name', required=True, translate=True)
    description = fields.Text('Property Description', required=True)
    date_availability = fields.Date(copy=False, default=lambda self: fields.Date.today() + timedelta(days=3))
    postcode = fields.Char('Postal Code')
    selling_price = fields.Float('Selling Price', readonly=True, copy=False, default=1000000)
    expected_price = fields.Float('Expected Price', required=True)
    bedrooms = fields.Integer('No of. Bedrooms', default=2)
    living_area = fields.Integer('Living Area')
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Garage', default=False)
    garden = fields.Boolean('Garden', default=False)
    garden_area = fields.Integer('Garden Area')
    garden_orientation = fields.Selection(
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West'),
        ],
        string='Garden Orientation',
        default='north'
    )
    sold = fields.Boolean('Sold', default=False)
    active = fields.Boolean('Active', default=True)
    state = fields.Selection(
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled'),
        ],
        string='State',
        default='new',
        required=True,
        copy=False
    )
    property_type_id = fields.Many2one("estate.property.type", string='Property Type')
    buyer_id = fields.Many2one('res.partner', string='Buyer')
    salesperson_id = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.user)
