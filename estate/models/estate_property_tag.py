from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Tags to describe estate properties"

    name = fields.Char(required=True)

    _check_name_unique = models.Constraint(
        'UNIQUE(name)',
        "The property tag's name must be unique."
    )
