from odoo import models, fields


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Type of properties"

    name = fields.Char(required=True)

    _unique_type = models.Constraint(
        'unique(name)',
        'The type name must be unique',
    )
