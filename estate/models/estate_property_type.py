from odoo import models, fields


class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Type of Property"
    _sql_constraints = [
        ("unique_type_name", "UNIQUE(name)", "The name of a property type must not already exist"),
    ]

    name = fields.Char(required=True)
