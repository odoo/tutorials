from odoo import fields, models


class estatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Tag for properites"
    _order = "name"

    name = fields.Char(string="Tag name", required=True)
    color = fields.Integer(string="color")

    _sql_constraints = [
        (
            "unique_property_tag",
            "unique(name)",
            "A tag with same property tag already exist",
        ),
    ]
