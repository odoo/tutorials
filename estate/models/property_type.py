from odoo import fields, models


class PropertyType(models.Model):
    _name = "property.type"
    _description = "Property Type"

    name = fields.Char(required=True)

    property_ids = fields.One2many(
        "estate.property", "property_type_id", string="Properties"
    )

    # sql constraints for unique property type name
    _sql_constraints = [
        ("unique_property_type", "unique(name)", "This property type already exists!")
    ]
