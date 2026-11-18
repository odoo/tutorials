from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Define a type of property"

    name = fields.Char(required=True)

    _check_unique_name = models.Constraint(
        'UNIQUE (name)',
        'The property type name must be unique.',
    )    