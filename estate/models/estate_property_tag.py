from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"
    _order = "name"

    name = fields.Char(required=True)
    color = fields.Integer()

    _unique_name = models.UniqueIndex(
        "(name)",
        "Another entry with the same name already exists.",
    )
