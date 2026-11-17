from odoo import models


from odoo import fields, models


class Property(models.Model):
    _name = "estate.property"
    _description = "Property"

    name = fields.Char('Name', required=True)
    expected_price = fields.Float('Expected Price', digits=(12, 2), required=True)
    description = fields.Char('Description')

    date_availability = fields.Date()
    selling_price = fields.Float('Selling Price', digits=(12, 2))
    postcode = fields.Char('Postcode')
    bedrooms = fields.Integer('# Bedrooms')
    facades = fields.Integer('# Facades')
    living_area = fields.Integer('Living area')
    garden_area = fields.Integer('garden area')
    garden_orientation = fields.Selection(
        string='Orientation', 
        selection = [('N', 'North'), ('S', 'South'), ('E', 'East'), ('W', 'West')])

    garage = fields.Boolean('Has a Garage', default=False)
    garden = fields.Boolean('Has a Garden', default=False)

    _check_living_area = models.Constraint(
        "CHECK(living_area >= 0)",
        "The living area surface has to be positive."
    )
    _check_garden_area = models.Constraint(
        "CHECK(garden_area >= 0)",
        "The garden area surface has to be positive."
    )
    _check_bedrooms = models.Constraint(
        "CHECK(bedrooms >= 0)",
        "The bedroom number has to be positive."
    )
    _check_facades = models.Constraint(
        "CHECK(facades >= 0)",
        "The facade number has to be positive."
    )

