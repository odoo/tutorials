from odoo import fields, models

class EstateProperty(models.Model):


    _name = 'estate.property'
    _description = 'Real Estate'

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_available = fields.Date()
    expected_price = fields.Float(required=True)
    selling_price = fields.Float()
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string="Type",
        selection=[("east", "East"), ("west", "West"), ("north", "North"), ("south", "South")],
    )
