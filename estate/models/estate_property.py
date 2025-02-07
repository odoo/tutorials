from odoo import models,fields,api 
from dateutil.relativedelta import relativedelta

class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = "This property is for sell"

    def _default_name(self):
        return self.get_value()
    
    name = fields.Char("Property Name", required=True)
    active = fields.Boolean(default=True)
    description = fields.Text("Description")
    postcode = fields.Char("Postal Code")
    date_availability = fields.Date("Availability Date", copy=False, default= lambda self: fields.Datetime.now() + relativedelta(months=3))
    expected_price = fields.Float("Expected Price", required=True)
    selling_price = fields.Float("Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer("Number of bedrooms", default=2)
    living_area = fields.Integer("Living Area")
    facades = fields.Integer("Facades")
    garage = fields.Boolean("Garage")
    garden = fields.Boolean("Garden")
    garden_area = fields.Integer("Garden Area")
    color = fields.Integer(string='Color')
    garden_orientation = fields.Selection(string='Garden Orientation',
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')
        ])
    state = fields.Selection(
        selection = [
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled')
        ],
        required=True, copy=False, default="new"
    )
