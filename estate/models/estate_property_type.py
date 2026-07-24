from odoo import fields, models


class PropertyType(models.Model):
    _name = 'estate.property.type'
    _description = "Estate Property Type"

    name = fields.Char(required=True)

    _unique_type_name = models.Constraint(
        'UNIQUE(name)',
        'A type name must be unique.',
    )
