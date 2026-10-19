from odoo import fields, models


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate properties declaration"

    name = fields.Char("Name", required=True)
    description = fields.Text("Description")
    postcode = fields.Char("Postcode")
    date_availability = fields.Datetime("Date_availability")
    expected_price = fields.Float("Expected_price", required=True)
    selling_price = fields.Float("Selling_price")
    bedrooms = fields.Integer("Bedrooms")
    living_area = fields.Integer("Living_area")
    facades = fields.Integer("Facades")
    garage = fields.Boolean("Garage")
    garden = fields.Boolean("Garden")
    garden_area = fields.Integer("Garden_area")
    garden_orientation = fields.Selection(
        string='Orientation',
        selection=[('north', 'North'), ('east', 'East'), ('south', 'South'), ('west', 'West')],
        help="Orientation is used to specify which cardinal direction the main facade faces."
    )
