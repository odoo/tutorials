from odoo import fields, models


class PropertyTagModel(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag model"
    _order = "name"
    _check_tag_uniqueness = models.Constraint(
        "UNIQUE(name)",
        "Each tag should have a unique name."
    )

    name = fields.Char(required=True)
    color = fields.Integer()
