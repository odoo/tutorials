from odoo import models, fields

class House(models.Model):
    _name = 'house'

    name = fields.Char(string='House Name', required=True)
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
    garden_orientation = fields.Selection(selection=[('S', 'South'),
                                           ('N', 'North'),
                                           ('W', 'West'),
                                           ('E', 'East')])
    



