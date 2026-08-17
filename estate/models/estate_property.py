from odoo import fields, models

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"
    # _order = ... ?


    name = fields.Char('Property Name', required=True, translate=True)
    description = fields.Text('Description', translate=True)
    postcode = fields.Char('Post Code', required=True)
    date_availability = fields.Date('Availability Date', required=True)

    expected_price = fields.Float('Expected Price')
    selling_price = fields.Float('Selling Price')

    bedrooms = fields.Integer('# Bedrooms')
    facades = fields.Integer('# Facades')

    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')

    living_area = fields.Integer('Living Area mt²')
    garden_area = fields.Integer('Garden mt²')
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West'),
        ] 
    )
