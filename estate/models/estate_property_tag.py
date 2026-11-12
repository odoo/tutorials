from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Estate Property Tag'
    _order = 'name'

    name = fields.Char('Property Tag', required=True)
    color = fields.Integer('Color')

    _name_uniq = models.Constraint(
        'unique(name)',
        'A property tag must be unique',
    )
