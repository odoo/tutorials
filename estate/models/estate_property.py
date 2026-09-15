from odoo import fields, models


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"

    name = fields.Char('Name', required=True)
    description = fields.Text('Description')
    postcode = fields.Char('Postcode')
    date_availability = fields.Date('Availability Date')
    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float('Selling Price')
    bedrooms = fields.Integer('Number of Bedrooms')
    living_area = fields.Integer('Living Area')
    facades = fields.Integer('Number of Facades')
    garage = fields.Boolean('is Garage')
    garden = fields.Boolean('is Garden')
    garden_area = fields.Integer('Garden Area')
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West")],
    )
