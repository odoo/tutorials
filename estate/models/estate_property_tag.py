from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"

    name = fields.Char(string="Property Tags", required=True)
    _name_uniq = models.Constraint(
        "unique(name)",
        "A tag with the same name is already exists.",
    )
