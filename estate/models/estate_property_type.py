from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"

    name = fields.Char(string="Name", required=True)

    _unique_name = models.Constraint(
        "UNIQUE (name)",
        "Name must be unique",
    )
