from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"

    name = fields.Char(required=True, string="Property Type Name")

    _name_uniq = models.Constraint(
        "unique (name)",
        "Property Type name must be unique",
    )
