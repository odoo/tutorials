from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"

    name = fields.Char(required=True)

    _type_name_unique_constraint = models.Constraint(
        "UNIQUE (name)", "Type name must be unique"
    )
