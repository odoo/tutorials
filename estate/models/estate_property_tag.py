from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag Ayve"
    _order = "name"
    color = fields.Integer()

    _sql_constraints = [
        (
            "unique_property_tag",
            "unique(name)",
            "A Property Tag with the same name already exists in the Database!"
        )
    ]

    name = fields.Char(required=True)
