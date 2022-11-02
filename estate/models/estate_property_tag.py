from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Estate Property Tag'
    _order = "name asc"

    name = fields.Char(required=True)
    color = fields.Integer('Color')

    _unique_constraints = models.Constraint(
        definition='UNIQUE(name)',
        message='The tag name must be unique',
    )
