from odoo import models, fields


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type"

    name = fields.Char(required=True)

    _unique_name = models.Constraint(
        'unique(name)',
        'The property type name must be unique.',
    )
