from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Types of real estate property"

    name = fields.Char(required=True)

    _sql_constraints = [
        ("name_uniq", "unique(name)", "Property type already exists!"),
    ]
