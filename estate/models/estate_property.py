from odoo import fields, models

class EstateProperty(models.Model):
    _name = "estate.estate.property"
    _description = "Real Estate Properties to sell"
    _order = "sequence"

    name = fields.Char()
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date()
    date_availability = fields.Date()
    expected_price = fields.Float()
    selling_price = fields.Float()
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
            string='Orientation',
            selection=[('north', 'North'), ('south', 'South'),('east', 'East'),('west', 'West')],
            help="Orientation of the garden of the property")
