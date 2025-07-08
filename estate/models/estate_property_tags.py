from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Tags For Estate Properties"
    _order = "name"

    name = fields.Char(required=True, string="Tag")
    color = fields.Integer('Color')

    _sql_constraints = [
        ("unique_tag_name", "UNIQUE(name)", "Tag name must be unique."),
    ]
