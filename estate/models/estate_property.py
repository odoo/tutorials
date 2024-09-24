from odoo import fields, models

class EstateProperty (models.Model):
    _name = "estate.property"
    _description = "real estate property"

    # Basic fields
    name = fields.Char(required = True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date()
    expected_price = fields.Float(required = True)
    selling_price = fields.Float()
    bedrooms = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string = 'Type',
        selection = [('North','N'), ('South','S'), ('East','E'), ('West','W')],
        help = "list of tuples descripting the orientation")

