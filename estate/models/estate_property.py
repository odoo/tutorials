from odoo import models, fields


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property model"


    name = fields.Char('Name', required = True)
    description = fields.Text('description')

    postcode = fields.Char()
    date_availability = fields.Date
    expected_price = fields.Float()
    selling_price = fields.Float()
    bedrooms = fields.Integer("# of bedrooms")
    living_area = fields.Integer("")
    facades = fields.Integer("# facades")
    garage = fields.Boolean("Has garage")
    garden = fields.Boolean("Has garden")
    garden_orientation = fields.Selection(
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West'),
        ],
        string="Garden Orientation"
    )




