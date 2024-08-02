from odoo import  models, fields


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "test"   

    name = fields.Char('Name',required = True)
    postcode = fields.Char('Postcode')
    date_availability = fields.Date('Date available')
    expected_price = fields.Float('Expected Price',required = True)
    selling_price = fields.Float('Selling Price')
    bedrooms = fields.Integer('Bedroom')
    living_area = fields.Integer('Living Area')
    facades = fields.Integer('Facade')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden Area')
    garden_orientation = fields.Selection(
        string='Orientation',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        help="Direction of the garden")

