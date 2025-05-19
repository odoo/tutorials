from odoo import fields, models


class Properties(models.Model):
    _name = "estate_property"
    _description = "Properties of the estate model"

    name = fields.Char("Title", required=True)
    description = fields.Text("description")
    postcode = fields.Integer("Post code")
    date_availability = fields.Date("Date availability")
    expected_price = fields.Float("Expected price", required=True)
    selling_price = fields.Float("Selling price")
    bedrooms = fields.Integer("# Bedrooms")
    living_area = fields.Integer("Living area")
    facades = fields.Integer("# facades")
    garage = fields.Boolean("Garage", default=False)
    garden = fields.Boolean("Garden", default=False)
    garden_area = fields.Integer("Garden area", default=0)
    garden_orientation = fields.Selection(
        string="Orientation",
        selection=[("north", "North"), ("east", "East"), ("west", "West"), ("south", "South")])
