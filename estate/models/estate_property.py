from odoo import fields, models


class estateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate property database table"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date()
    expected_price = fields.Float(required=True)
    selling_price = fields.Float()
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection=[ ('north','North'),('south','South'), ('east','East'), ('west','West') ] )