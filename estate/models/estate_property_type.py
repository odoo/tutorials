from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"

    name = fields.Char(required=True)
    property_ids = fields.One2many("estate.property", "property_type_id", string="Properties")

    _unique_type_name = models.Constraint(
        "UNIQUE(name)",
        "A property type name must be unique.",
    )
