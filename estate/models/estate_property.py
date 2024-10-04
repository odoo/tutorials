from datetime import date, timedelta
from odoo import fields, models  # type: ignore

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property Application Ayve"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(default=lambda self: (date.today() + timedelta(days=90)).strftime('%Y-%m-%d'))
    expected_price = fields.Float()
    selling_price = fields.Float(readonly=True)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        [
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')
        ],
        string='Garden Orientation',
        help='Select One Orientation'
    )

    active = fields.Boolean(default=True)
    
    status = fields.Selection(
        [
            ('available', 'Available'),
            ('sold', 'Sold'),
            ('pending', 'Pending')
        ],
        string='Status',
        default='available',
        help='Select the current status of the property'
    )
