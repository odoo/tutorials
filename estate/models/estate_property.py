from odoo import fields, models


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate property"





    name = fields.Char('Property Name', required=True, translate=True)
    address = fields.Char('Address', required=True, translate=True)
    postcode = fields.Char('Postal Code', required=True, translate=True)
    description = fields.Text('Description', translate=True)
    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float('Selling Price', required=True)
    bedrooms = fields.Integer('# Bedrooms', required=True)
    living_area = fields.Integer('Living Area', required=True)
    facades = fields.Integer('# Facades', required=True)
    garden = fields.Boolean('Garden', required=True)
    garden_area = fields.Integer('Garden Area', required=True)
    garden_orientation = fields.Selection(
        string='Garden Orientation', 
        selection=[('north', 'North'), ('east', 'East'), ('south', 'South'), ('west', 'West')], 
        translate=True)
    garage = fields.Boolean('Grage', required=True)
    availability = fields.Date('Date', required=True)
