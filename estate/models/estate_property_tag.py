from odoo import models, fields


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Estate Property Tag'
    _order = 'name'

    name = fields.Char(string='Name', required=True)
    color = fields.Integer('Color')
#   Constraints:
    _check_unique = models.Constraint(
        'UNIQUE (name)',
        'The tag name must be unique'
    )
