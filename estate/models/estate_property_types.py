from odoo import fields, models


class PropertyTypeModel(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type model"
    _check_type_uniqueness = models.Constraint(
        "UNIQUE(name)",
        "Each type should have a unique name."
    )

    name = fields.Char(required=True)
