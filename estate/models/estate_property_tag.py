from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tags"
    _order = "name asc"

    name = fields.Char(required=True)
    color = fields.Integer("Color")

    _sql_constraints = [
        ("name_unique", "UNIQUE(name)", "Tag already exists"),
    ]
