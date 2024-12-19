
from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "The type of a property"
    _order = "name"

    _sql_constraints = [
        (
            "name",
            "unique(name)",
            "The name of the property type must be unique.",
        )
    ]

    name = fields.Char(required=True)
    properties_ids = fields.One2many("estate.property", string="Properties", inverse_name="property_type_id")
    sequence = fields.Integer("Sequence", default=1)
