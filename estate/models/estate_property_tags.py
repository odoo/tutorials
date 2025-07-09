from odoo import fields, models


class EstatePropertyTags(models.Model):
    _name = "estate.property.tags"
    _description = "Estate Property Tags"
    _order = "name"

    _sql_constraints = [
        ("_unique_tag_name", "UNIQUE(name)", "Tag name must be unique.")
    ]

    name = fields.Char(required=True)
    color = fields.Integer(default=3)
