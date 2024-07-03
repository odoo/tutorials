from odoo import models, fields


class Testing(models.Model):
    _name = "estate_property"
    _description = "This is Real Estate"

    name = fields.Char('prop_Name', required=True, translate=True)
    description = fields.Text('Description')
    postcode = fields.Char('Postcode')
    date_availability = fields.Date('Date_avail')
    expected_price = fields.Float('exp_price', required=True)
    selling_price = fields.Float('sell_price')
    bedrooms = fields.Integer('bedrooms')
    living_area = fields.Integer('live_area')
    facades = fields.Integer('facades')
    garage = fields.Boolean('garage')
    garden = fields.Boolean('garden')
    garden_area = fields.Integer('gar_area')
    garden_orientation = fields.Selection(
        string='Type',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')]
    )
