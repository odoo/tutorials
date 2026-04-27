from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"
    name = fields.Char('Property Tag Name', required=True)

    _unique_name = models.Constraint(
        "UNIQUE(name)",
        "Property tag names must be unique.",
    )
