from odoo import models, fields


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate Property'

    name = fields.Char('Property name', required=True, translate=True)
    description = fields.Text('Property description', translate=True)
    postcode = fields.Char('Property postcode')
    date_availability = fields.Date('Date available')
    expected_price = fields.Float('Expected price', required=True)
    selling_price = fields.Float('Selling price')
    bedrooms = fields.Integer('Bedrooms')
    living_area = fields.Integer('Living area')
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Has garage', default=False)
    garden = fields.Boolean('Has garden', default=False)
    garden_area = fields.Integer('Garden area')
    garden_orientation = fields.Selection(
        string='Garden orientation',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        help='Garden orientation is important for determining how much sunlight and warmth the outdoor space receives'
    )
