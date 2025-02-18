from odoo import fields, models


class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real estate property type"

    name = fields.Char("Property Type", required=True)

    _sql_constraints = [
        ("type_name_unique", "unique (name)", "The type name should be unique.")
    ]
