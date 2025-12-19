from odoo import fields, models


class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type"

    name = fields.Char(name="Name", required=True)

    # Constraints
    _check_unique_name = models.Constraint("UNIQUE(name)", "A property type name must be unique")
