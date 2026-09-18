from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate property tag model"

    name = fields.Char(required=True)

    _property_tag_unique_constraint = models.Constraint(
        "UNIQUE(name)",
        "Property tag should have an unique name!"
    )
