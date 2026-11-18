from odoo import models, fields


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Estate Property Tags'

    name = fields.Char(required=True)

    _no_duplicates = models.Constraint(
        'UNIQUE(name)',
        'A tag name must be unique'
    )
