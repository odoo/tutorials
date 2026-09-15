from odoo import fields, models

class TestModel(models.Model):
    _name = "estate_property_model"
    _description = "Estate property model test description"

    name = fields.Char('Estate Property Model Name', required=True)
    description = fields.Text("Description of the Estate Propert Model")
    postcode = fields.Char("5000")
    date_availability = fields.Date("2026-09-15")
    expected_price = fields.Float(required=True)
    selling_price = fields.Float()
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([("north", "North"), ("south", "South"), ("west", "West"), ("east", "East")])

    