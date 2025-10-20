from odoo import fields, models

class EstateProperty(models.Model):
    _name = "estate_property"
    _description = "Real estate propreties"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date()
    expected_price = fields.Float()
    selling_price = fields.Float(required=True)
    bedrooms = fields.Float()
    living_area = fields.Float()
    facades = fields.Float()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Float()
    garden_orientation = fields.Selection(
        selection=[('north', 'North'), ('south', 'South'), ('west', 'West'), ('east', 'East')]
    )