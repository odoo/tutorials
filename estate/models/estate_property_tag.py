from odoo import fields, models


class EstatePropertyTags(models.Model):
    _name = "estate.property.tag"
    _description = "This table contain the types of tags"

    name = fields.Char(required=True)

    _name_uniq = models.Constraint(
        "unique(name)",
        "Tag name is must be Unique",
    )
