from odoo import models, fields


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"

    _check_unique_name = models.Constraint(
        'UNIQUE (name)',
        'Tag names must be unique.',
    )

    name = fields.Char(required=True)
