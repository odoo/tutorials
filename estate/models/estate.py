from odoo import fields, models

class Estate(models.Model):
    _name = "estate_property"
    _description = "Estate Property Module"

    name = fields.Char(string="Title", required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    expected_date = fields.Float(string="Expected Date", required=True)
    selling_price = fields.Float(string="Selling Price", required=True)
    bedroom = fields.Integer(string="Number of Bedroom")
    living_area = fields.Integer(string="Living area (square metter)")
    facades = fields.Integer(string="Number of facades")
    garage = fields.Boolean(string="Have a garage?")
    garden = fields.Boolean(string="Have a garden?")
    garden_area = fields.Integer(string="Garden area (square metter)")
    garden_orientation = fields.Selection(string="Garden's orientation", selection=[('north', 'North'), ('sud', 'Sud'), ('east', ' East'), ('west', 'West')])
