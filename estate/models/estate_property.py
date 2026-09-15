from odoo import fields, models


class EstatePropertyModel(models.Model):
    _name = "estate_property"
    _description = "The details of a property"

    name = fields.Char('Estate Name', required = True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date()
    expected_price = fields.Float(required = True)
    selling_price = fields.Float()
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Integer()
    has_garage = fields.Boolean()
    has_garden = fields.Boolean()
    garden_orientation= fields.Selection(string='Type',
                                        selection=[('east', 'East'),
                                                    ('west', 'West'),
                                                    ('north', 'North'),
                                                    ('south', 'South')
                                                    ]
                                        )
