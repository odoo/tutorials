from odoo import fields, models


class PropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Property Types'

    name = fields.Char("Type", required=True)

    _sql_constraints = [
        ("check_unique_type", "UNIQUE(name)",
         "The type name should be unique."),
    ]