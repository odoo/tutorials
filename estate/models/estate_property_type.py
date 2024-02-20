from odoo import fields, models

class EstateModel(models.Model):
    _name = "estate.property.type"
    _description = "Estate/Property/Type"

    name = fields.Char(required=True)

    _sql_constraints = [
        ("property_type_unique", "unique (name)", "The property type name must be unique")
    ]
