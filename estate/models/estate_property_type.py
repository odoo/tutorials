from odoo import models, fields


class EstatePropertyType(models.Model):
    _name = "estate.property.types"
    _description = "Estate Property Types"

    name = fields.Char("Property Type", required=True)

    _check_type_name = models.Constraint(
        'UNIQUE(name)',
        'The type name should be unique.',
    )
