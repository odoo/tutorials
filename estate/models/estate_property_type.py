from odoo import _, fields, models


class EstatePropertyType(models.Model):
    _name = "realestate.properties.type"
    _description = "Real estate property type"

    name = fields.Char("Property type", required=True)
    _unique_name = models.Constraint(
        "UNIQUE(name)",
        _("Property name already exists. Property names must be unique."),
    )
