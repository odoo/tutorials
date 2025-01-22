from odoo import models, fields
from datetime import date, timedelta
class EstateProperty(models.Model):

    _name = "estate.property"
    _description = "Damn this model is good for doing real estate related stuff"

    name = fields.Char(name = "Title", required=True)
    description = fields.Text(name = "Description", required = True)
    postcode = fields.Char(name = "PostCode", required = True)
    date_availability = fields.Date(name = "Availability", default=lambda self: date.today() + timedelta(days=90), copy=False)
    expected_price = fields.Float(name="Expected Price")
    selling_price = fields.Float(name = "Selling Price", readonly = True, copy = False)
    bedrooms = fields.Integer(name = "Bedrooms", default = 2)
    living_area = fields.Integer(name = "Living Area (m²)")
    facades = fields.Integer(name = "Facades")
    garage = fields.Boolean(name = "Garage")
    garden = fields.Boolean(name = "Garden")
    garden_area = fields.Integer(name = "Garden Area (m²)")
    garden_orientation = fields.Selection(string='Garden orientation',
        selection=[('north', 'North'), 
                   ('west', 'West'), ('south', 'South'), 
                   ('east', 'East')
                   ],
        help="Chose the direct which the garden is facing")
    
    active = fields.Boolean(default=True)
    state = fields.Selection(string='Status',
        selection=[('new', 'New'), 
                   ('offer received', 'Offer received'), 
                   ('offer accepted', 'Offer accepted'), 
                   ('sold', 'Sold'), 
                   ('cancelled', 'Cancelled')
                   ],
        help="Is the house sold already ?")
