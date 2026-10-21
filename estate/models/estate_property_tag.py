from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"

    name = fields.Char(required=True)

    _tag_name_unique_constraint = models.Constraint(
        "UNIQUE (name)", "Tag name must be unique"
    )
