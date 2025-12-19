from odoo import fields, models


class PropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Real Estate Property Tag"

    name = fields.Char(name="Name", required=True)

    # Constraints
    _check_unique_name = models.Constraint("UNIQUE(name)", "A property tag name must be unique")
