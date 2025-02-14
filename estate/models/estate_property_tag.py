from odoo import api, exceptions, fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Different Tags to describe the aesthetics of Property"
    _order = "name"

    name = fields.Char("Property Tag", required=True)
    color = fields.Integer(string="Color", default=0)

    _sql_constraints = [
        (
            "unique_property_tag_name",
            "UNIQUE(name)",
            "The property tag name must be unique.",
        )
    ]
