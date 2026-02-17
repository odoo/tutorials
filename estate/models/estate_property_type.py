from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property Type"

    name = fields.Char(required=True)
    property_ids = fields.One2many(
    "estate.property",      # target model
    "property_type_id",     # field in that model pointing back
    string="Properties",    # label shown in UI
    )

    _unique_name = models.Constraint(
        "UNIQUE(name)",
        "Property type name must be unique."
    )
