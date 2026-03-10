from odoo import models, fields


class Estate_Property(models.Model):
    _name = "estate.property"
    _description = "Real estate system"

    name = fields.Char(string="Property Name", required=True)
    description = fields.Text()
    postcode = fields.Char(string="Postal Code")
    date_availability = fields.Date(string="Availability Date")
    expected_price = fields.Float(string="Expected Selling Price", required=True)
    selling_price = fields.Float(string="Selling Price")
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')])
