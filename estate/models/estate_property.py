from odoo import fields, models
from dateutil.relativedelta import relativedelta


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = "estate property description"
    name = fields.Char('Property Name', required=True)
    address = fields.Char('Property Address', required=True)
    postcode = fields.Char('Property Postcode', required=True)
    expected_price = fields.Float('Property Expected Price', digits=(16, 2), required=True)
    availability_date = fields.Date('Property Available', required=True, copy=False, default=lambda _ : fields.Date.today() + relativedelta(months=3))
    furnished = fields.Boolean('Property Furnished', required=True, default=False)
    bedrooms = fields.Integer('Property Bedrooms', required=True, default=2)
    bathrooms = fields.Integer('Property Bathrooms', required=False, default=1)
    selling_price = fields.Float('Property Selling Price', digits=(16, 2), required=False, readonly=True, copy=False)
    living_area = fields.Integer('Property Living Area', required=False)
    garage = fields.Boolean('Property Has Garage', required=True)
    garden = fields.Boolean('Property Has Garden', required=True)
    garden_area = fields.Integer('Property Garden Area (sqm)', required=True)
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        help="orientation of the garden")
    active = fields.Boolean('Property Active', default=True)
    state = fields.Selection(string='Property State', selection=[('new', 'New'),
                                                                 ('offer_received', 'Offer Received'),
                                                                 ('offer_accepted', 'Offer Accepted'),
                                                             ('sold', 'Sold'), ('cancelled', 'Cancelled')],
                             default='new', required=True, copy=False)
    facades = fields.Integer('Property Facades')
    description = fields.Text('Property Description', default="No description provided.")