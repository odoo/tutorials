from dateutil.relativedelta import relativedelta
from odoo import fields,models

class EstateProperty(models.Model):
    _name='estate.property'
    _descripion='Estate Property description modulee'
    name=fields.Char(string='Name',required=True)
    description=fields.Text(string='Description')
    bedrooms=fields.Integer(string='Bedrooms',default=2)
    price = fields.Float(string='Price')
    garden = fields.Boolean(string='Garden')
    postcode = fields.Char(string='Postal Code')
    date_available = fields.Date(string='Available Date',copy=False,default=lambda self:fields.Date.today() + relativedelta(months=3))
    expected_price = fields.Float(string='Expected Price')
    selling_price = fields.Float(string='Selling Price',readonly=True,copy=False)
    meeting_time = fields.Datetime(string='Meeting')
    living_area = fields.Integer(string='Living Area')
    facades = fields.Integer(string='Facades')
    garage = fields.Boolean(string='Garage')
    garden = fields.Boolean(string='Garden')
    garden_area = fields.Integer(string='Garden Area')
    garden_orientation=fields.Selection(
        [
            ('north','North'),('south','South'),('east','East'),('west','West')
        ]
    )
    active=fields.Boolean(default=True)
    state=fields.Selection(
        [
            ('new','New'),('offer_received','Offer Received'),('offer_accepted','Offer Accepted'),('sold','Sold'),('canceled','Canceled')
        ],
        default='new',
        string='Status',
        copy=False,
        required=True
    )
