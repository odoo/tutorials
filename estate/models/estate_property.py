from odoo import models, fields

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "test description"

    name =  fields.Char('Name', required=True)
    description = fields.Text('Description')
    postcode = fields.Char('Post Code')
    date_availability = fields.Date('Date availability')
    expected_price = fields.Float('Expected price', required=True)
    selling_price = fields.Float('Selling price')
    bedrooms = fields.Integer('Bedrooms')
    living_area = fields.Integer('Living area')
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden area')
    garden_orientation = fields.Selection(
        string='Orientation',
        selection=[('north','North'), ('east','East'), ('south','South'), ('west','West')],
    )