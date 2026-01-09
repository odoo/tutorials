from odoo import fields, models


class EstatePropertyTypes(models.Model):
    _name = "estate.property.type"
    _description = "This is table contain the types of property"
    _order = "name asc"

    name = fields.Char(required=True)
    property_ids = fields.One2many("estate.property", "property_type_id")

    _name_uniq = models.Constraint(
        "unique(name)",
        "Property Types must be Unique",
    )
