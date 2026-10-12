from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "this model defines property type"
    _order = "name"

    name = fields.Char("Type", required=True)
    property_ids = fields.One2many("estate.property", "property_type_id")

    _name_uniq = models.Constraint(
        "unique (name)",
        "A property type name must be unique",
    )
