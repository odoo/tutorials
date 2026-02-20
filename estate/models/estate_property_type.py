from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "estate property type"

    name = fields.Char(string="Property Category", required=True)
    property_type_id = fields.Integer()

    _check_name_unique = models.Constraint(
        "unique(name)",
        "The Property type must be unique.",
    )
