from odoo import fields, models

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "this is the estate property model"
    name = fields.Char('Property Name', required=True)
    description = fields.Text('Description')
    postcode = fields.Char('Postal Code')
    date_availability = fields.Date()
    expected_price = fields.Float(digits=(20, 2), required=True)
    selling_price = fields.Float(digits=(20, 2))
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(selection=[
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West')])
    _sql_constraints = []
