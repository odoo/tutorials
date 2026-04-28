from odoo import fields, models


class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property Types"

    name = fields.Char(required=True)

    _check_name = models.Constraint(
    'UNIQUE(name)',
    'A property type name must be unique',
    )
