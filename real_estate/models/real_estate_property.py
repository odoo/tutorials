from odoo import fields, models
from dateutil.relativedelta import relativedelta

class RealEstate(models.Model):
    _name = "real.estate.property"
    _description = 'Real State propperties'

    name = fields.Char(string = 'Title', required = True)
    description = fields.Text(string = 'Description')
    postcode = fields.Char(string = 'Postcode')
    date_availability = fields.Date(string = 'Available From', copy = False, default = fields.Datetime.now() + relativedelta(months=3))
    expected_price = fields.Float(string = 'Expected Price', required = True)
    selling_price = fields.Float(string = 'Selling Price', readonly = True, copy = False)
    bedrooms = fields.Integer(string = 'Bedrooms', default = 2)
    living_area = fields.Integer(string = 'Living Area (sqm)')
    facades = fields.Integer(string = 'Facades')
    garage = fields.Boolean(string = 'Garage')
    garden = fields.Boolean(string = 'Garden')
    garden_area = fields.Integer(string = 'Garden Area (sqm)')
    garden_orientation = fields.Selection(
        [
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')

        ],
        string = 'Garden Orientation'

    )
    status = fields.Selection(
        [
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled')
        ],
        default = 'new',
        string = 'Status',
        copy = False
    )
    active = fields.Boolean(string = "Active", default = True)




    