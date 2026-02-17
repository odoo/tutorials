from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Types"

    name = fields.Char(string="Property Types", required=True)
    _name_uniq = models.Constraint(
        "unique(name)",
        "A Property Type with the same name already exists.",
    )
