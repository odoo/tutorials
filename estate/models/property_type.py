from odoo import models, fields


class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property Type"

    name = fields.Char(string="Name", required=True)
    _name_uniq = models.Constraint(
        "UNIQUE (name)",
        "The name of the type must be unique!",
    )
