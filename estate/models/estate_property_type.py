from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property type"

    name = fields.Char(required=True)

    _sql_constraints = [
        ("check_type_name", "UNIQUE(name)", "The type name must be unique")
    ]
