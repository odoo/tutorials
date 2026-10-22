from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"

    name = fields.Char(required=True)

    _property_type_name_uniq = models.Constraint(
        'UNIQUE(name)',
        'A property type name must be unique'
    )
