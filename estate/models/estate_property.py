from odoo import models, fields

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Property for the Real Estate app"


    #Adding fields
    name = fields.Char(required=True)
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
    garder_area = fields.Integer()
    garden_orientation = fields.Selection(selection=[("North", "north"), ("South", "south"), ("East", "east"), ("West", "west")])



