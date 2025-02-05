from odoo import models,fields

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = 'description for esate'

    name = fields.Char(string = 'Name', required = True)
    description = fields.Text(string = 'Description')
    postcode = fields.Char(string = 'PostCode', index = True)
    date_availability = fields.Date(string = 'Available Date', default= lambda self:fields.Date.add(fields.Date.today(), months=3), copy = False)
    expected_price = fields.Float(string = 'Expected Price', required = True)
    selling_price = fields.Float(string = 'Selling Price', readonly = True)
    bedrooms = fields.Integer(string = 'Bedrooms', default = 2)
    living_area = fields.Integer(string = 'Living Area')
    facades = fields.Integer(string = 'Facades', help="a facade refers to the front or exterior appearance of a building, usually facing the street.")
    garage = fields.Boolean(string = 'Garage')
    garden = fields.Boolean(string = 'Garden') 
    garden_area = fields.Integer(string= 'Gaarden Area')
    garden_orientation = fields.Selection([('north','North'), ('south', 'South'), ('west', 'West'), ('east', 'East')])
