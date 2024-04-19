from odoo import fields, models

class PropertyType(models.Model):

    _name = "estate_property_type"
    _description = "The type of the real estate property i.e. house, apartment, etc"
    _sql_constraints = [
        ('unique_name', 'unique(name)', 'The name of the property type must be unique'),
    ]
    name = fields.Char(required=True)
