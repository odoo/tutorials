from odoo import fields, models


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "property data"

    name = fields.Char('name', required=True)
    description = fields.Text('desc')
    postcode = fields.Char('postcode')
    date_availability = fields.Date()
    expected_price = fields.Float()
    selling_price = fields.Float()
    bedrooms = fields.Integer('# Bedrooms')
    living_area = fields.Integer('living.area.size')
    facades = fields.Integer('# Facades')
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer('garden.size')
    garden_orientation = fields.Selection(
        string='Orientation',
        selection=[('North', 'North'), ('West', 'West'), ('East', 'East'), ('South', 'South')]
    )
