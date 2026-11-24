from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property Type"
    _order = "sequence, name"
    
    name = fields.Char(required=True)
    sequence = fields.Integer(default=10)
    _sql_name_unique = models.Constraint(
        "UNIQUE(name)",
        "Property type already exists.",
    )