from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Property Tags"

    name = fields.Char("Name", required=True)

    _sql_constraints = [
        ("name_uniq", "unique (name)", "Each name must be unique."),
    ]
