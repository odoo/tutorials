from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate property Type"
    _sql_constraints = [
        ("check_name", "UNIQUE(name)", "A type must be unique."),
    ]

    name = fields.Char(string="Name")
