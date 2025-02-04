from odoo import fields, models


class EstateProperty(models.Model):
    _name = "estate.estate.property"
    _description = "Estate property"

    name = fields.Char('Property Name', required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date('Date of Availability')
    expected_price = fields.Float(required=True)
    selling_price = fields.Float()
    bedrooms = fields.Integer('No. of Bedrooms')
    living_area = fields.Integer()
    facades = fields.Integer()
    active = fields.Boolean(default=True)
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection = [('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')]
    )