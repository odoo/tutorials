from odoo import _, fields, models


class EstatePropertyTag(models.Model):
    _name = "realestate.properties.tag"
    _description = "Real estate property tag"

    name = fields.Char("Name", required=True)
    _unique_name = models.Constraint(
        "UNIQUE(name)",
        _("Tage name already exists. Tag names must be unique."),
    )
