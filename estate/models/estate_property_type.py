from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type"

    name = fields.Char(required=True)

    _sql_constraints = [
        ("estate_property_type_check_name", "UNIQUE(name)", "The property type already exists"),
    ]
