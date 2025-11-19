from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'All property tags'

    name = fields.Char(required=True)

    _check_unique_name = models.Constraint(
        'unique (name)',
        'The name of a tag should be unique.',
    )
