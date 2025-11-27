from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Estate Property Tags'
    _order = 'name asc'

    name = fields.Char(required=True)
    color = fields.Integer()

    _check_unique_name = models.Constraint(
        'unique (name)',
        'The name of a tag should be unique.',
    )
