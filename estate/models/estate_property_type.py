from odoo import fields, models


class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "describe the type property"

    name = fields.Char(required=True)

    # SQL constraints
    _sql_constraints = [
        ('name_unique', 'unique(name)',
         'The name of a property type should be unique'),
    ]
