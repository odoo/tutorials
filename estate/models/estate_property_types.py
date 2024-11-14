from odoo import models, fields


class EstatePropertyType(models.Model):
    _name = "estate.property.types"
    _description = "Real Estate Property Type"

    name = fields.Char(required=True, string="Property Type")

    _sql_constraints = [
        ("check_property_type", "UNIQUE(name)", "Property type must be unique"),
    ]
