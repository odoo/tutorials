from odoo import fields, models


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Model"

    name = fields.Char(string="Name")
    description = fields.Text(string="Description")
    postcode = fields.Text(string="Postcode")
    date_availability = fields.Date(string="Date Availability")
    expected_price = fields.Float(string="Expected Price")
    selling_price = fields.Integer(string="Selling Price")
    bedrooms = fields.Integer(string="Bedrooms")
    living_area = fields.Integer(string="Living Area")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area")
    garden_orientation = fields.Selection(
        string="Type",
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
    )
