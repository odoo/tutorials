from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Estate Property Tag'

    name = fields.Char(required=True)

    _check_name = models.Constraint(
        'UNIQUE(name)',
        'This property tag already exists, try something else.'
    )
