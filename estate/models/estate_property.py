from odoo import models,fields


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate Property'

    id = fields.Integer(string='ID', required=True, readonly=True)
    create_uid = fields.Integer(string='Created by', readonly=True)
    create_date = fields.Datetime(string='Creation Date', readonly=True)
    write_uid = fields.Integer(string='Last Updated by', readonly=True)
    write_date = fields.Datetime(string='Last Updated Date', readonly=True)
    
    name = fields.Char(string='Property Name', required=True)
    description = fields.Text(string='Description')
    postcode = fields.Char(string='Postcode')
    date_availability = fields.Date(string='Date Availability')
    expected_price = fields.Float(string='Expected Price')
    selling_price = fields.Float(string='Selling Price')
    bedrooms = fields.Integer(string='Number of Bedrooms')
    living_area = fields.Integer(string='Living Area (m²)')
    facades = fields.Integer(string='Number of Facades')
    garage = fields.Boolean(string='Has Garage')
    garden = fields.Boolean(string='Has Garden')
    garden_area = fields.Integer(string='Garden Area (m²)')
    garden_orientation = fields.Char(string='Garden Orientation')
