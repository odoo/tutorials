from odoo import fields, models


class EstateProperTag(models.Model):
    _name = "estate.property.tag"
    _description = "Property Tag."
    _order = "name"

    name = fields.Char('Property Tag', required=True)
    color = fields.Integer('Color')

    _check_name = models.Constraint(
        'UNIQUE(name)',
        'The tag must be unique.',
    )
