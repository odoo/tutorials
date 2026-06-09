from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"

    name = fields.Char(required=True)

    _name_unique = models.Constraint(
        "UNIQUE(name)", "Property Type name must be unique."
    )

