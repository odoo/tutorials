from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"

    name = fields.Char(required=True)

    _check_name = models.Constraint(
        'UNIQUE(name)',
        'This property type already exists, try something else.'
    )
