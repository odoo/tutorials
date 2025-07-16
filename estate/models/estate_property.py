from odoo import  fields,models


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property is defined"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_avaiblity = fields.Date()
    expected_price = fields.Float(required=True)
    selling_price = fields.Float()
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string = 'Type',
        selection=[('north','North'), ('south','South'), ('east','East'), ('west','West')],
        help = "Orientation is used to locate garden's direction"
    )