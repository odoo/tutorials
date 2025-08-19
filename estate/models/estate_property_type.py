from odoo import models, fields


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"

    name = fields.Char(required=True)

    _sql_constraints = [
        ("unique_name", "UNIQUE(name)", "A type with same name is already exists."),
    ]
