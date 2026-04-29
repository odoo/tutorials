from odoo import fields, models


class Estate_property_tag(models.Model):
    _name = "estate.property.tag"
    _description = "tag super mega trop bien"
    _order = "name"

    name = fields.Char(required=True)
    color = fields.Integer()

    _check_name = models.Constraint(
        "UNIQUE(name)",
        message="The name of the tag must be unique",
    )
