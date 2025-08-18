from odoo import models, fields


class EstatePropertyTags(models.Model):
    _name = "estate.property.tags"
    _description = "Estate Property Tags"
    _sql_constraints = [
        (
            "estate_property_tag_name_unique",
            "UNIQUE(name)",
            "The tag names must be unique.",
        )
    ]

    _order = "name"

    name = fields.Char(string="Tag Name", required=True)
    color = fields.Integer(string="Color Index")
