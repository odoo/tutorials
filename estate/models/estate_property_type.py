from odoo import models, fields


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type"
    _order = "name"

    name = fields.Char(required=True)
    property_ids = fields.One2many(
        "estate.property", "property_type_id", string="Properties"
    )
    sequence = fields.Integer()

    _unique_name = models.Constraint(
        "UNIQUE(name)",
        "The name of the property type must be unique",
    )
