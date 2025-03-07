from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _order="name"

    name = fields.Char(string="Property Type", required=True)
    property_ids = fields.One2many("estate.property", "property_type_id", string=" ")

    _sql_constraints = [
        ("unique_property_type_name", "unique(name)", "Property Type already exists.")
    ]
