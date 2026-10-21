from odoo import fields, models


class PropertyTags(models.Model):
    _name = "estate.property.tag"
    _description = "Real Estate Property Tags"
    _order = "name"

    name = fields.Char(string="Name", required=True)
    color = fields.Integer()

    _check_name = models.Constraint(
        "unique (name)",
        "A property tag name must be unique.",
    )
