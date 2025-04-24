from odoo import models, fields


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate property type"
    _sql_constraints = [
        ("check_unique_name", "UNIQUE(name)", "Property type name must be unqie")
    ]

    name = fields.Char('name', required=True)
