from odoo import models, fields


class PropertyType(models.Model):
    _name = "estate.property.tag"
    _description = "Real estate property tag"
    _order = "name"

    _sql_constraints = [
        ("name_uniq", "unique (name)", "Tag already exists")
    ]

    name = fields.Char("Name", index=True, translate=True, required=True)
    color = fields.Integer("Color", required=True)