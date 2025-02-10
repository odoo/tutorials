from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"

    name = fields.Char(required=True)
    # all_properties_ids = fields.One2many("estate.property", "property_type_id", string="All Properties")

    _sql_constraints = [
        ("unique_name", "UNIQUE(name)", "A type with same name is already exists."),
    ]
