from odoo import fields, models


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate property"
    _order = "sequence"

    name = fields.Char("Estate Name", required=True, translate=True)
    description = fields.Text("Description")
    postcode = fields.Char("PostCode")
    date_availability = fields.Date("Date Availability")
    expected_price = fields.Float("Expected price")
    selling_price = fields.Float("Selling price")
    bedrooms = fields.Integer("Bedrooms")
    living_area = fields.Integer("Living area")
    facades = fields.Integer("Facades")
    garage = fields.Boolean("Garage")
    garden = fields.Boolean("Garden")
    garden_area = fields.Integer("Garden Area")
    garden_orientation = fields.Selection(
        [("n", "North"), ("s", "South"), ("w", "West"), ("e", "East")]
    )
