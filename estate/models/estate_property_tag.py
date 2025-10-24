from odoo import models, fields


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"

    name = fields.Char(required=True)

    _unique_property_tag_name = models.Constraint(
        "UNIQUE(name)",
        "The tag name must be unique.",
    )
