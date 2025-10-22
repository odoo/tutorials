from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Define the type of the property"

    _check_unique_type = models.Constraint(
        'UNIQUE(name)',
        'Type already exists.',
    )
    name = fields.Char(required=True)
