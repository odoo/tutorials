from odoo import models, fields


class Estate(models.Model):
    _name = "estate_property"
    _description = "Real Estate management module"
    _order = "sequence"

    name = fields.Char(string="Name of the property", required=True)
    description = fields.Text(string="Description")
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
    garden_orientation = fields.Selection([('n', 'North'), ('e', 'East'), ('s', 'South'), ('w', 'West')])
