from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate property type"

    name = fields.Char(required=True)
    property_ids = fields.One2many("estate.property", "property_type_id")
    _sql_constraints = [
        ("unique_property_type", "UNIQUE(name)", "Property type should be unique")
    ]
