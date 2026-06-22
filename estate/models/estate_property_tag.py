from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Real Estate Property Tag"
    _order = "name"

    _name_uniq = models.Constraint(
        "unique(name)",
        "A tag with the same name already exists.",
    )

    name = fields.Char("Title", required=True)
    color = fields.Integer()
