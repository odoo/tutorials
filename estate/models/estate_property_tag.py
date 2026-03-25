from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Real Estate Property Tag"
    _order = "name"

    name = fields.Char(string="Tag Name", required=True)
    color = fields.Integer(string="Color")

    _unique_tag_name = models.Constraint(
        "UNIQUE(name)",
        "Property tag name must be unique.",
    )
