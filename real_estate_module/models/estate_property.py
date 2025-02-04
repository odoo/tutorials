from odoo import models, fields

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"

    name = fields.Char(required=True)              # Property name
    create_uid=fields.Char(required=True)
    create_date=fields.Char(required=True)
    description = fields.Text()                    # Description
    postcode = fields.Char()                       # Postcode
    date_availability = fields.Date()              # Available date
    expected_price = fields.Float(required=True)   # Expected price
    selling_price = fields.Float()                 # Selling price
    bedrooms = fields.Integer()                    # Number of bedrooms
    living_area = fields.Integer()                 # Size of the property
    facades = fields.Integer()                     # Number of facades
    garage = fields.Boolean()                      # Does it have a garage?
    garden = fields.Boolean()                      # Does it have a garden?
    garden_area = fields.Integer()                 # Garden size
    garden_orientation = fields.Selection(         # Garden direction
        [('north', 'North'), 
         ('south', 'South'), 
         ('east', 'East'), 
         ('west', 'West')]
    )
