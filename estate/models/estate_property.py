from odoo import models, fields


class EstateModel(models.Model):
    _name = "estate_property"
    _description = "Real Estate"
    _order = "sequence"

    name = fields.Char('Name', required=True)
    description = fields.Char('Description')
    post_code = fields.Char('Post Code')
    date_availability = fields.Date('Available From')
    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float('Selling Price')
    bedrooms = fields.Integer('Bedrooms Count')
    living_area = fields.Float('Living Area size')
    facades = fields.Integer('Number of facades')
    garage = fields.Boolean('Has garage')
    garden = fields.Boolean('Has garden')
    garden_area = fields.Integer('Garden area')
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        help="Garden orientation selection"
    )
