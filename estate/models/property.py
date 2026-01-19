from odoo import fields, models

class EstateProperty(models.Model):
    _name = "estate_property"
    _description = "estate property"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(string="Date availability")
    expected_price = fields.Float(string="Expected price", required=True)
    selling_price = fields.Float(string="Selling price")
    bedrooms = fields.Integer()
    living_area = fields.Integer(string="Living area")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string="Garden area")
    garden_orientation = fields.Selection(string="Garden orientation", selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')])