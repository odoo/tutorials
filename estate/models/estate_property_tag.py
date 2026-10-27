from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate property tag"
    _order = "name asc"

    name = fields.Char('Property Tag', required=True)
    color = fields.Integer('Color', default=0)
    _check_duplicates = models.Constraint(
        'UNIQUE(name)',
        'This tag already exist',
    )
