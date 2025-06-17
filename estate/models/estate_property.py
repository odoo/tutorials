from odoo import fields, models

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Store Real Estate Properties"

    name = fields.Char("Estate Name", required=True, translate=True)
    description = fields.Text("Description", help="Enter the real estate item description")
    postcode = fields.Char("Postcode")
    date_availability = fields.Datetime("Available From")
    expected_price = fields.Float("Expected Price", digits=(16, 1))
    selling_price = fields.Float("Selling Price", digits=(16, 1))
    bedrooms = fields.Integer("Bedrooms", default=1, help="Number of bedrooms in the property")
    living_area = fields.Integer("Living Area (m²)")
    facades = fields.Integer("Facades", help="Number of building facades")
    garage = fields.Boolean("Garage", default=False)
    garden = fields.Boolean("Garden", default=False)
    garden_area = fields.Integer("Garden Area (m²)", default=0)
    garden_orientation = fields.Selection(
        [
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')
        ],
        string="Garden Orientation",
        help="Direction the garden faces"
    )
