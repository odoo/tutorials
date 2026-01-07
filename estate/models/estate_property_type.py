from odoo import fields, models


class EstatePropertyTypes(models.Model):
    _name = "estate.property.type"
    _description = "This is table contain the types of property"

    name = fields.Char(required=True)

    _name_uniq = models.Constraint(
        "unique(name)",
        "Property Types must be Unique",
    )
