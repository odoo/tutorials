from odoo import fields, models
from odoo.tools import date_utils


class Property(models.Model):
    _name = "estate.property"
    _description = "Estate property"

    name = fields.Char('Property Name', required=True)
    description = fields.Text('Property Description')
    active = fields.Boolean(default=True)
    state = fields.Selection(
        string='Current Status',
        selection=[('new','New'), ('offer_received','Offer Received'), ('offer_accepted','Offer Accepted'), ('sold','Sold'), ('cancelled','Cancelled')],
        default='new',
        required=True
    )
    postcode = fields.Char('Postcode')
    date_availability = fields.Date('Availability Date', default=lambda self: date_utils.add(fields.Datetime.today(),months=3), copy=False)
    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float('Selling Price', readonly=True, copy=False)
    bedrooms = fields.Integer('Bedrooms', help="Number of bedrooms", default=2)
    living_area = fields.Integer('Living Area (m²)')
    facades = fields.Integer('Facades', help="Number of facades")
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden Area (m²)')
    garden_orientation = fields.Selection(
        string='Orientation',
        selection=[('north','North'),('south','South'),('east','East'),('west','West')],
        help="Indicates the orientation of the garden"
    )