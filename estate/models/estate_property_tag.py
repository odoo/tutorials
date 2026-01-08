from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"

    name = fields.Char(required=True)

    _name_unique = models.Constraint(
        'unique(name)',
        'The Property Tag must be unique.',
    )
