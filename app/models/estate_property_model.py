from odoo import fields, models


class EstatePropertyModel(models.Model):
    _name = "estate.property.model"
    _description = "Real Estate Property"
    _order = "name"

    name = fields.Char('Property Name', required=True, translate=True)
    description = fields.Text('Property Description', required=True)
    date_availability = fields.Date()
    postcode = fields.Char('Postal Code')
    selling_price = fields.Float('Selling Price')
    expected_price = fields.Float('Expected Price', required=True)
    bedrooms = fields.Integer('No. of Bedrooms')
    living_area = fields.Integer('Living Area')
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Active', default=True)
    garden = fields.Boolean('Active', default=False)
    garden_area = fields.Integer('Garden Area')
    garden_orientation = fields.Selection(
        selection=[
            ('male', 'Male'),
            ('female', 'Female'),
            ('other', 'Other')
        ],
        string='Gender',
        default='male'
    )
    sold = fields.Boolean('Active', default=True)
