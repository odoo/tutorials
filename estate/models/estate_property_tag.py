from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Estate Property Tag'
    _order = 'name'

    name = fields.Char(string='Property Tag', required=True)
    color = fields.Integer(string='Color')

    _name_uniq = models.Constraint(
        'unique(name)',
        'A property tag must be unique',
    )
