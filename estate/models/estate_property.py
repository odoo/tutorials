

from odoo import fields, models


class EstateProperty(models.Model):
    _name: str = "estate.propety"

    name: fields.Char = fields.Char()
    description: fields.Text = fields.Text()
    postcode: fields.Char = fields.Char()
    date_availability: fields.Date = fields.Date('Creation Date')
    expected_price: fields.Float = fields.Float()
    selling_price: fields.Float = fields.Float()
    bedroom: fields.Integer = fields.Integer()
    living_area: fields.Integer = fields.Integer()
    facades: fields.Integer = fields.Integer()
    garage: fields.Boolean = fields.Boolean()
    garden: fields.Boolean = fields.Boolean()
    garden_area: fields.Integer = fields.Integer()
    garden_orientation: fields.Selection(
        string='Type',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        help="Type is used to separate Leads and Opportunities")

