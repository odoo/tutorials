from odoo import models, fields
from dateutil.relativedelta import relativedelta


class EstateModel(models.Model):
    _name = "estate_property"
    _description = "Real Estate"

    name = fields.Char('Name', required=True)
    description = fields.Char('Description')
    post_code = fields.Char('Post Code')
    state = fields.Selection(
        string="State",
        selection=[('new', 'New'), ('offer received', 'Offer Received'), ('offer accepted', 'Offer Accepted'), ('sold', 'Sold'), ('canceled', 'Canceled')],
        help="Estate current state",
        required=True,
        default='new',
        copy=False
    )
    date_availability = fields.Date('Available From', copy=False, default=lambda self: fields.Date.today() + relativedelta(months=3))
    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float('Selling Price', readonly=True, copy=False)
    bedrooms = fields.Integer('Bedrooms Count', default=2)
    living_area = fields.Float('Living Area size')
    facades = fields.Integer('Number of facades')
    garage = fields.Boolean('Has garage')
    garden = fields.Boolean('Has garden')
    garden_area = fields.Integer('Garden area')
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        help="Garden orientation selection"
    )
    active = fields.Boolean('Is Active', default=True)
