from odoo import models, fields

class EstateProperties(models.Model):
    _name = "estate.properties"
    _description = "Real Estate Properties"
    # _log_access = False
    
    name = fields.Char('Property Name', required=True, help="Name of the property shown")
    description = fields.Text('Description', help="Description of the property shown")
    postcode = fields.Char('Postcode', help="Postal Code of the property shown")
    date_availability = fields.Date('Availability Date', help="Date of availability of the property shown")
    expected_price = fields.Float('Expected Price', required=True, help="Expected price of the property shown")
    selling_price = fields.Float('Selling Price', help="Selling Price of the property shown")
    bedrooms = fields.Integer('Bedrooms', help="Number of bedrooms in the property shown")
    living_area = fields.Integer('Living Area', help="Number of living rooms in the property shown")
    facades = fields.Integer('Facades', help="Number of facades in the property shown")
    garage = fields.Boolean('Has Garage?', help="Does the proeprty have a garage?")
    garden = fields.Boolean('Has Garden?', help="Does the property have a garden?")
    garden_area = fields.Integer('Garden Area', help="Area of the garden of the property shown")
    garden_orientation = fields.Selection([('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')], help="Directional orientation of the garden of the property shown")

