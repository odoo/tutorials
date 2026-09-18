from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Estate Property Tag'

    name = fields.Char(required=True)

    _unique_constraints = models.Constraint(
        definition='UNIQUE(name)',
        message='The tag name must be unique',
    )
