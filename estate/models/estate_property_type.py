from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type"

    _name_uniq = models.Constraint(
        'UNIQUE(name)',
        'The property type name must be unique.',
    )

    name = fields.Char(required=True)
