from odoo import models, fields

class Property(models.Model):
    _name = "estate.property"
    _description = "Estate property model"

    name = fields.Char(string='Name', required=True, help='This is the name of the estate property.', index=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date()
    expected_price = fields.Float(required=True)
    selling_price = fields.Float()
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(string='Type', selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')])