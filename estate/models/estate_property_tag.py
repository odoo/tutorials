from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate property tag"

    name = fields.Char('Property Tag', required=True)

    _check_duplicates = models.Constraint(
        'UNIQUE(name)',
        'This tag already exist',
    )
