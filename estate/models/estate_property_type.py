from odoo import fields, models


class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate type"
    
    _sql_constraints = [
        ('check_name', 'UNIQUE(name)',
         'A property Type must be unique.'),
    ]

    name = fields.Char(required=True)
