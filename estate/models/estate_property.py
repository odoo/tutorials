from odoo import models, fields

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"

    name = fields.Char(string = 'Name', required=True)
    description = fields.Text(string = 'Description' , translate = True)
    postcode = fields.Char(string = 'Postcode')
    date_availability = fields.Date(string = 'Date Availability')
    expected_price = fields.Float(string = 'Expected Price', required=True)
    selling_price = fields.Float(string = 'Selling Price')
    bedrooms = fields.Integer(string = 'Bedrooms')
    living_area = fields.Integer(string = 'Living Area')
    facades = fields.Integer(string = 'Facades')
    garage = fields.Boolean(string = 'Garage')
    garden = fields.Boolean(strings = 'Garden')
    garden_area = fields.Integer(string = 'Garden Area')
    garden_orientation = fields.Selection(selection = [('north','North',),('south','South',),('east','East',),('west','West',)], string = 'Garden Orientation',)


    

