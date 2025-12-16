from odoo import models, fields   

class buildings_model(models.Model):
    _name = 'estate.buildings'
    _description = 'Buildings Model'

    name = fields.Char()
    description = fields.Text()
    value = fields.Integer()
    garden_orientation = fields.Selection(
        'Garden Orientation',
        [
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')
        ]
    )

    