from odoo import fields, models

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property Name"

    name = fields.Char('Property name', required = True)
    selling_price = fields.Integer('Property Price')
    description = fields.Text('Property description')
    postcode = fields.Char('Postcode')
    date_avaibility = fields.Datetime('Date of publish')
    expected_price = fields.Float('Expected price', required = True)
    bedrooms = fields.Integer('No.of bedrooms')
    living_area = fields.Integer('Area')
    facades = fields.Integer('facade')
    garage = fields.Boolean('Available')
    garden = fields.Boolean('Present')
    garden_area = fields.Integer('Garden Area')
    garden_orientation = fields.Selection(
        string = 'Type',
        selection = [
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')]
    )
