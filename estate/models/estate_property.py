from odoo import fields, models


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property discription"

    name = fields.Char('name', required=True)
    description = fields.Text('description')
    postcode = fields.Char('postcode')
    date_availability = fields.Date('availabilty date')
    expected_price = fields.Float('expected price', required=True)
    selling_price = fields.Float('selling price')
    bedrooms = fields.Integer('bedrooms')
    living_area = fields.Integer('living area')
    facades = fields.Integer('facades')
    garage = fields.Boolean('garage')
    garden_area = fields.Integer('garden area')
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[('North', 'North'), ('South', 'South'),
                   ('East', 'East'), ('West', 'West')]
    )
