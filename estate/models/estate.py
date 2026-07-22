from odoo import api, fields, models

class Estate(models.Model):
    _name = 'estate_property'
    _description = 'Real Estate'

    name = fields.Char('Name', required=True)
    description = fields.Text('Description')
    postcode = fields.Char('Postcode')
    date_availability = fields.Date("Date Available")
    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float('Selling price')
    bedrooms = fields.Integer("Bedrooms")
    living_area = fields.Integer("Living Area")
    facades = fields.Integer("Facades")
    garage = fields.Boolean("Garage")
    garden = fields.Boolean("Garden")
    garden_area = fields.Integer("Garden Area")
    garden_orientation = fields.Selection(string="Garden Orientation",
                            selection=[('north', 'North'), ('east', 'East'), ('west', 'West'), ('south', 'South')])
