from odoo import fields, models


class Property(models.Model):
    _name = "estate.property"
    _description = "estate property info"

    name = fields.Char(required=True, translate=True)
    description = fields.Text(translate=True)
    postcode = fields.Char()
    date_availability = fields.Date()
    expected_price = fields.Float(required=True)
    selling_price = fields.Float()
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden_area = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(string='garden_orientation' , selection=[('North','north'),('east','East'),('West','west'),('South','south')])
    