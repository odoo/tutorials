from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Estate Property Tag'

    name = fields.Char(required=True)

    _tag_name_uniq = models.Constraint(
        'unique (name)',
        'The tag name must be unique.',
    )
