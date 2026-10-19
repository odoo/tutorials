from odoo import fields, models  # ty: ignore[unresolved-import]


class PropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Tag of real estate property"

    name = fields.Char(required=True)
