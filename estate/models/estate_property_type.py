from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _order = "sequence, name"

    name = fields.Char(required=True)
    property_ids = fields.One2many(
        "estate.property", "property_type_id", string="Property"
    )
    sequence = fields.Integer("Sequence")

    _sql_constraints = [
        ("unique_name", "UNIQUE(name)", "The property type must be unique.")
    ]
