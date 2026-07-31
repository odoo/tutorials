from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Real estate property tag"
    _order = "name"

    name = fields.Char("Name", required=True)
    color = fields.Integer()

    _unique_name = models.Constraint(
        "UNIQUE(name)",
        "Tage name already exists. Tag names must be unique.",
    )
