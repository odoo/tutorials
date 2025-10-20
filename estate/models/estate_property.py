from odoo import models, fields

class EstateProperty(models.model):
    _name = "estate_property"
    _description = "Table that stores the estate properties"

    name = fields.Char(string="Title", required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")

    date_availability = fields.Date(string="Available From")
    expected_price = fields.Float(string="Expected price", required=True)
    selling_price = fields.Float(string="Selling price")
    bedrooms = fields.Integer(string="Bedrooms")
    living_area = fields.Integer(string="Living Arez (sqm)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection=[
            ('north', 'North'), 
            ('south', 'South'), 
            ('east', 'East'), 
            ('west', 'West')
        ]
    )
