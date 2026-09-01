from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"

    name = fields.Char(required=True)
    property_ids = fields.One2many(
        "estate.property", "property_type_id", string="Properties"
    )

    _unique_name = models.Constraint(
        "UNIQUE(name)",
        "The property type name must be unique.",
    )
