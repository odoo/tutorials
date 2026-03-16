from odoo import models, fields

class EstateProperty(models.Model):
    _name = "estate.property"

    name = fields.Char(required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char()
    date_availability = fields.Date(string="Date Availability")
    expected_price= fields.Float(required=True)
    selling_price= fields.Float()
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([('north', "North"),('east', "East"),('south', "South"),('west', "West")])