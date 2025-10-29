from odoo import models, fields
from dateutil.relativedelta import relativedelta


class EstateProperty(models.Model):
    _name = 'estate_property'
    _description = "Real Estate Property"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=fields.Date.today() + relativedelta(months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation=fields.Selection(string='Garden Orientation',selection=[('north', 'North'), ('south', 'South'), ('east','East'), ('west','West')])
    active=fields.Boolean(default=False)
    state=fields.Selection(selection=[('new','New'),('offer_received','Offer Received'),('offer_accepted','Offer Accepted'),('sold','Sold'),('cancelled','Cancelled')])
        
