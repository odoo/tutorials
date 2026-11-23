from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Property Tag"
    _order = "name"

    name = fields.Char(required=True, string="Tag")
    color = fields.Integer(default=0)

    _check_name = models.Constraint(
        "UNIQUE(name)",
        "This tag name already exists"
    )
