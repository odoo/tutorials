from odoo import models, fields


class EstateProperty(models.Model):
    _name = "estate_property"
    _description = "real estate properties"

    name = fields.Char(default="Unknown")

    availability_date = fields.Date('Availability', copy=False)
    selling_price = fields.Float('Selling Price', readonly=True, copy=False)
    bedrooms = fields.Integer('Bedrooms', default=2)
    last_seen = fields.Datetime("Last Seen", default=fields.Datetime.now)
    expected_price = fields.Float('Expected Price', required=True)
    facades = fields.Integer('Facades', required=True)
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    active = fields.Boolean(default=True)
    state = fields.Selection(
        string='Property State',
        selection=[
            ('new', 'New'),
            ('offer Received', 'Offer Received'),
            ('offer Accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled')
        ],
    )
