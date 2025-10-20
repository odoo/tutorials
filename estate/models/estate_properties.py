from odoo import fields, models

class PropertyModel(models.Model):
    _name = "estate.property"
    _description = "Estate Property model"

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
        string='Orientation',
        selection=[
            ('North', 'north'),
            ('South', 'south'),
            ('East', 'east'),
            ('West', 'west')
        ]
    )
