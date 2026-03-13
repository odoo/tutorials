from odoo import fields, models
from dateutil.relativedelta import relativedelta


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate Property'

    name = fields.Char(string='Title', required=True, default='Unknown')
    description = fields.Text(string='Description')
    postcode = fields.Char(string='Postal Code')
    last_seen = fields.Datetime(
        string="Last Seen", default=fields.Datetime.now)
    date_availability = fields.Date(
        string='Available From', copy=False, default=fields.Date.today() + relativedelta(months=+3)
    )
    expected_price = fields.Float(string='Expected Price', required=True)
    selling_price = fields.Float(
        string='Selling Price', readonly=True, copy=False)
    living_area = fields.Float(string='Area (sq m)')
    bedrooms = fields.Integer(string='Bedrooms', default=2)
    facades = fields.Integer(string='Facades')
    has_garage = fields.Boolean(string="Has Garage ?")
    has_garden = fields.Boolean(string="Has Garden ?")
    garden_area = fields.Integer(string="Garden Area (sq m)")
    active = fields.Boolean(string="Is Active ?", default=True)
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[('north', 'North'),
                   ('south', 'South'),
                   ('east', 'East'),
                   ('west', 'West')],
    )
    state = fields.Selection(
        string="Status",
        selection=[("New", "New"),
                   ("Offer Received", "Offer Received"),
                   ("Offer Accepted", "Offer Accepted"),
                   ("Sold", "Sold"),
                   ("Cancelled", "Cancelled")],
        required=True, default="New", copy=False
    )
