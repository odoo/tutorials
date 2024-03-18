from odoo import models, fields

class EstateProperty(models.Model):
    _name = "estate.property"
    _description= "model for real estate assets"
    
    name = fields.Char('Name', required = True)
    description = fields.Text('Description')
    postcode = fields.Char('Postcode')
    date_availability = fields.Date('Available date', default = lambda _: fields.Date.add(fields.Date.today(), months=3))
    expected_price = fields.Float('Expected Price', required = True)
    selling_price = fields.Float('Selling Price')
    bedrooms = fields.Integer('# bedrooms', default = 2)
    living_area = fields.Integer('Living Area (m2)')
    facades = fields.Integer('# facades')
    garage = fields.Boolean('Has Garage')
    garden = fields.Boolean('Has Garden')
    garden_area = fields.Integer('Garden Area (m2)')
    garden_orientation = fields.Selection( [ ('North', ''), ('South', ''), ('East', ''), ('West', '') ] )

