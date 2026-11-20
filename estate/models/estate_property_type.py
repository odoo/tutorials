from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type"

    name = fields.Char(required=True)

    _check_unique_type = models.Constraint(
        'UNIQUE(name)',
        "Type name should be unique.",
    )
