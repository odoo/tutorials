from odoo import models, fields


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property Model"

    name = fields.Char("Property Name", required = True)
    description = fields.Text("Description")
    postcode = fields.Char("Postcode")
    date_availability = fields.Date("Availability Date")
    expected_price = fields.Float("Expected Price", required = True)
    selling_price = fields.Float("Selling Price")
    bedrooms = fields.Integer("Num of Bedrooms")
    living_area = fields.Integer("Num of Living Areas")
    facades = fields.Integer("Facades")
    garage = fields.Boolean("Garage")
    garden = fields.Boolean("Garden")
    garden_area = fields.Integer("Garden Area")
    garden_orientation = fields.Selection(string="Garden Orientation", selection=[('north', 'North'), ('east', 'East'), ('south', 'South'), ('west', 'West')])