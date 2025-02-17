from odoo import fields, models


class EstatePropertyModel(models.Model):
    _name = "estate.property"
    _description = "Defines the model of a real estate property"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(string="Date of availability")
    expected_price = fields.Float(required=True, string="Expected price")
    selling_price = fields.Float(string="Selling price")
    bedrooms = fields.Integer(string="Number of bedrooms")
    living_area = fields.Integer(string="Living area")
    facades = fields.Integer(string="Number of facades")
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string="Garden area")
    garden_orientation = fields.Selection(
        [("north", "North"), ("south", "South"), ("east", "East"), ("west", "West")],
        string="Garden orientation",
    )
