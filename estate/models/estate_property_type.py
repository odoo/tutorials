from odoo import models, fields


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "estate property type"

    name = fields.Char(required=True)

    _unique_name = models.Constraint(
        'UNIQUE(name)',
        'The name must be unique',
    )
