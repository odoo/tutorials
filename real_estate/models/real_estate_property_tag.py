from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "This are tags used to identify property"
    _order = "name"

    name = fields.Char(required=True)
    color = fields.Integer()

    _check_tag_name = models.Constraint(
        "UNIQUE(name)",
        "Tag name Must be unique",
    )
