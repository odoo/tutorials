from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate property Tag"
    _sql_constraints = [
        ("check_name", "UNIQUE(name)", "A tag must be unique."),
    ]

    name = fields.Char(string="Name")
