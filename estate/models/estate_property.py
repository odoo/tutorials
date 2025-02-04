from dateutil.relativedelta import relativedelta
from odoo import fields, models

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Properties"

    name = fields.Char('Name',required = True)
    description = fields.Text('Description')
    postcode = fields.Char('Postcode')
    date_availability = fields.Date('Available From',copy = False,default = lambda self:fields.Date.add(fields.Date.today()+ relativedelta(months=3)))
    expected_price = fields.Float('Expected Price', required = True)
    selling_price = fields.Float('Selling Price ', readonly = True, copy = False)
    bedrooms = fields.Integer('Bedrooms', default = 2)
    living_area = fields.Integer('Living Area(sqm)')
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden Area(sqm)')
    garden_orientation = fields.Selection(
        string = 'Garden Orientation',
        selection = [('north','North'),('south','South'),('east','East'),('west','West')]
    )
    active = fields.Boolean('Active',default=True)
    status = fields.Selection(
        selection = [('new','New'),('offer_received','Offer Received'),('offer_accepted','Offer Accepted'),('sold','Sold'),('cancelled','Cancelled')],
        string = 'Status',
        required = True,
        copy = False,
        default = 'new'
    )
