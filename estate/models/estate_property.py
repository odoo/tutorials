from odoo import fields, models

class estate_property(models.Model):
    _name = 'estate.property'
    _description = "estate property description"
    name = fields.Char('Property Name', required=True)
    address = fields.Char('Property Address', required=True)
    postcode = fields.Char('Property Postcode', required=True)
    expected_price = fields.Float('Property Expected Price', digits=(16, 2), required=True)
    available = fields.Date('Property Available', required=True)
    Furnished = fields.Boolean('Property Furnished', required=True)
    bedrooms = fields.Integer('Property Bedrooms', required=True)
    bathrooms = fields.Integer('Property Bathrooms', required=True)
    selling_price = fields.Float('Property Selling Price', digits=(16, 2), required=False)
    living_area = fields.Integer('Property Living Area', required=True)
    garage = fields.Boolean('Property Has Garage', required=True)
    garden = fields.Boolean('Property Has Garden', required=True)
    garden_area = fields.Integer('Property Garden Area', required=True)
    garden_orientation = fields.Selection(
        string='Type',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        help="orientation of the garden")
