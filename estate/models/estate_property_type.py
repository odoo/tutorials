from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property Type"
    _order = "sequence, name"

    sequence = fields.Integer(default=10)
    name = fields.Char(required=True)
    property_ids = fields.One2many(
    "estate.property",      
    "property_type_id",     
    string="Properties",
    )

    _unique_name = models.Constraint(
        "UNIQUE(name)",
        "Property type name must be unique."
    )
