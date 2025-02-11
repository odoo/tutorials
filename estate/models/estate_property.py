from odoo import models, fields

class estate_property(models.Model):
    _name = "estate_model"  
    _description = "This is the description for esatet properties model:"

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
        selection = [('north', 'North'), ('east', 'East'), ('south', 'South'),('west', 'West')]
    )