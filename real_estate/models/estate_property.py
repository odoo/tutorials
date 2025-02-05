from odoo import fields, models

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"

    name = fields.Char(string="Property Name", required=True, help="Enter the property name.")
    description = fields.Text(string="Description", help="Brief description of the property.")
    postcode = fields.Char(string="Postcode", help="Postal code of the property.")
    date_availability = fields.Date(string="Availability Date", default=fields.Date.today, help="Date when the property will be available.",copy=False  )
    expected_price = fields.Float(string="Expected Price", required=True, help="The price the seller expects.")
    selling_price = fields.Float(string="Selling Price", help="The final selling price of the property.",readonly=True,copy=False)
    bedrooms = fields.Integer(string="Bedrooms", default=2, help="Number of bedrooms in the property.")
    living_area = fields.Integer(string="Living Area (sq ft)", default=0, help="The size of the living area in square feet.")
    facades = fields.Integer(string="Facades", help="Number of facades the property has.")
    garage = fields.Boolean(string="Garage", help="Check if the property has a garage.")
    garden = fields.Boolean(string="Garden", help="Check if the property has a garden.")
    garden_area = fields.Integer(string="Garden Area (sq ft)", compute='_compute_garden_fields', store=True, help="Size of the garden in square feet.")
    garden_orientation = fields.Selection(
        [
            ('north', 'North'), 
            ('south', 'South'), 
            ('east', 'East'), 
            ('west', 'West')
        ],
        string="Garden Orientation", 
        help="Direction the garden faces."
    )
    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)', 'Expected price must be positive.'),
        ('check_selling_price', 'CHECK(selling_price >= 0)', 'Selling price cannot be negative.')
    ]

