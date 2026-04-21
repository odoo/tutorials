from odoo import fields, models


class EstateProperty(models.Model):
    _name = "estate_property"
    _description = "Lorem Ipsum technical description of a Real Estate object"

    name = fields.Char(
        required=True,
    )
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date()
    expected_price = fields.Float()
    selling_price = fields.Float()
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden_area = fields.Boolean()
    garden_orientation = fields.Selection(
        string='Orientation',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        help="If you don't know where West is, wait for the sun to go to sleep. Its bedroom lies West.",
    )
