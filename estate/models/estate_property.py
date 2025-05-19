from odoo import fields, models


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "estate property module"

    name = fields.Char(required=True)
    description = fields.Text()
    date_availability = fields.Date("Date Availability")
    expected_price = fields.Float("Expected Price", required=True)
    selling_price = fields.Float("Selling Price", default=0)
    bedrooms = fields.Integer(required=True)
    living_area = fields.Integer("Living Area (sqm)", required=True)
    facades = fields.Integer(default=0)
    garage = fields.Boolean(default=False)
    garden = fields.Boolean(default=False)
    garden_area = fields.Integer("Garden Area (sqm)")
    garden_orientation = fields.Selection([('north', 'North'), ('east', 'East'), ('south', 'South'), ('west', 'West')])
    total_area = fields.Integer("Total Area (sqm)", required=True)
