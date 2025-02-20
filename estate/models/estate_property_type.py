from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Model containing property type"

    name = fields.Char(required=True, default="Unknown")

    _sql_constraints = [
        (
            "check_unique_type",
            "unique (name)",
            "Type must be unique",
        )
    ]
