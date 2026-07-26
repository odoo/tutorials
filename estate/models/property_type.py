from odoo import fields, models


class PropertyType(models.Model):
    _name = "estate_property_type"
    _description = "The type of the property to be sold such as House, apartment, ..."

    name = fields.Char(string="Name", required=True)

    _unique_name = models.Constraint(
        "UNIQUE(name)",
        "Property type names must be unique!",
    )
