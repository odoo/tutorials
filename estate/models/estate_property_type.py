from odoo import models, fields


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property Type"
    _order = "name"

    name = fields.Char(string="Name", required=True)

    # Optional: Back-reference for all properties of this type (One2many)
    property_ids = fields.One2many(
        "estate.property", "property_type_id", string="Properties"
    )

    _sql_constraints = [
        (
            "unique_property_type_name",
            "UNIQUE(name)",
            "Property type name must be unique.",
        ),
    ]
