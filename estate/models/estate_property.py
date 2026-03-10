from odoo import fields, models


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate Property'

    name = fields.Char(string='Title', required=True)
    description = fields.Text(string='Description')
    postcode = fields.Char(string='Postal Code')
    date_availability = fields.Date(string='Available From')
    expected_price = fields.Float(string='Expected Price', required=True)
    selling_price = fields.Float(string='Price')
    living_area = fields.Float(string='Area (sq m)')
    bedrooms = fields.Integer(string='Bedrooms')
    facades = fields.Integer(string='Facades')
    has_garage = fields.Boolean(string="Has Garage ?")
    has_garden = fields.Boolean(string="Has Garden ?")
    garden_area = fields.Integer(string="Garden Area (sq m)")
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[('north', 'North'),
                   ('south', 'South'),
                   ('east', 'East'),
                   ('west', 'West')],
    )
