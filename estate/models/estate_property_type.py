from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate property type such as 'house'"

    name = fields.Char(required=True)

    _property_type_name_unique = models.Constraint(
        'UNIQUE(name)',
        'Property type names must be unique',
    )
