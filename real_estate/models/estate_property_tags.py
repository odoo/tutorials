from odoo import models, fields


class EstatePropertyTags(models.Model):
    _name = "estate.property.tags"
    _description = "Estate Property Tags"
    _order = "name"

    name = fields.Char(required=True)
    color = fields.Integer()

    _sql_constraints = [
        (
            "unique_tag_name",
            "UNIQUE(name)",
            "This property tag already exits, create a unique one.",
        )
    ]
