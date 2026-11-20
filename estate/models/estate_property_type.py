from odoo import fields, models


class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Type"

    name = fields.Char('Name', required=True)

    _check_name_uniq = models.Constraint(
        'UNIQUE (name)',
        "This type of property already exists.",
    )
