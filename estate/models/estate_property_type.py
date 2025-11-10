from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type"

    name = fields.Char(required=True)

    _check_type_name_unique = models.Constraint(
    'UNIQUE(name)', 
    'The name of the property type must be unique.'
    )
