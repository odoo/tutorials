from odoo import models, fields


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate property tag"
    _sql_constraints = [
        ("check_unique_name", "UNIQUE(name)", "Property tag must be unqie")
    ]

    name = fields.Char('name', required=True)
