from odoo import fields, models


class estatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Tag for properites"

    name = fields.Char(string="Tag name", required=True)

    _sql_constraints = [
        (
            "unique_property_tag",
            "UNIQUE(name)",
            "A tag woth same property tag already exist",
        ),
    ]
