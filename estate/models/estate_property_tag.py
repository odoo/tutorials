from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Model containing property tags"
    _order = "name"

    name = fields.Char(required=True)
    color = fields.Integer()

    _sql_constraints = [
        (
            "check_unique_tag",
            "unique (name)",
            "Tag must be unique",
        )
    ]
