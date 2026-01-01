from odoo import models

class EstateProperty(models.Model):
    _name = "estate_model"
    _description = "This is to say that this is the description of the Estate Model"
    
    name = fields.Char()
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date()
    expected_price = fields.Float()
    selling_price = fields.Float()
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string='Type',
        selection=[('east', 'East'), ('west', 'West'),('north', 'North'), ('south', 'South')],
        help="You can choose any direction of you own"
    )
