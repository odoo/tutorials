from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Property Tags"
    _order = "name"

    name = fields.Char("Name", required=True)
    color = fields.Integer("Color")

    _sql_constraints = [
        ("name_uniq", "unique (name)", "Each name must be unique."),
    ]
