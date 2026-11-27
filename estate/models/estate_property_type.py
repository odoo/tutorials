from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property Types"

    name = fields.Char(required=True)

    _unique_property_type_name = models.Constraint(
        'UNIQUE(name)',
        'Type name must be unique !'
    )
