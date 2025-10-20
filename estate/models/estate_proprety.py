from odoo import fields, models

class EstateProprety(models.Model):
    _name = "estate.proprety"
    _description = "Estate Proprety"


    name = fields.Char('Estate Name', required=True)
    description = fields.Text('Estate Description', required=True)
    postcode = fields.Char('Estate Postcode', required=True)
    date_availablity = fields.Date('Estate Availability Date', required=True)
    expected_price = fields.Float('Estate expected price', required=True)
    selling_price = fields.Float('Estate selling price', required=True)
    bedrooms = fields.Integer('Number of bedrooms', required=True)
    facades = fields.Integer('Number of facades')
    garage = fields.Boolean('Has a garage ?')
    garden = fields.Boolean('Has a garden ?')
    garden_area = fields.Integer('Garden area')
    garden_orientation = fields.Selection(
        string='Type',
        selection=[('north', 'North'), ('south', 'South'), ('west', 'West'), ('east', 'East')],
        help="Garden orientation selection"
    )
    