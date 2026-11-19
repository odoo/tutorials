from odoo import fields, models


class PropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Tag'

    name = fields.Char('Tag', required=True)

    _check_unique_name = models.Constraint(
        'UNIQUE(name)',
        'The name of a tag must be unique.',
    )
