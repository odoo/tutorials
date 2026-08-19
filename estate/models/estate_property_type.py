from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"

    name = fields.Char(required=True)
    _name_uniq = models.Constraint(
        "UNIQUE (name)",
        "The name of the property type must be unique!",
    )
