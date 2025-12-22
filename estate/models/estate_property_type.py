from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate property type"

    name = fields.Char(required=True)
    _unique_name = models.Constraint(
        "Unique(name)", "The property type must have a unique name"
    )
