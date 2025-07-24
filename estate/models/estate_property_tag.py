from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tags"

    name = fields.Char(required=True)

    _sql_constraints = [
        ("name_unique", "UNIQUE(name)", "Tag already exists"),
    ]
