from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Model containing property type"
    _order = "name"

    name = fields.Char(required=True, default="Unknown")
    property_ids = fields.One2many("estate.property", "property_type_id")

    _sql_constraints = [
        (
            "check_unique_type",
            "unique (name)",
            "Type must be unique",
        )
    ]
