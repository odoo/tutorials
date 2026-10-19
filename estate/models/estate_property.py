from odoo import fields, models


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate properties"

    title = fields.Char("Title", required=True)
    description = fields.Text("Description")
    postcode = fields.Char("Postcode")
    date_availability = fields.Date("Availability")
    expected_price = fields.Float("Expected Price", required=True)
    selling_price = fields.Float("Selling Price")
    bedrooms = fields.Integer("Bedrooms")
    living_area = fields.Integer("Living Area")
    facades = fields.Integer("Facades")
    garage = fields.Boolean("Has Garage")
    garden = fields.Boolean("Has Garden")
    garden_area = fields.Integer("Garden Area")
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[("nord", "Nord"), ("south", "South"), ("east", "East"), ("west", "West")]
    )
