from odoo import models, fields


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Tag for the property'
    _order = 'name'

    name = fields.Char(required=True)
    color = fields.Integer()

    _check_unique_name = models.Constraint(
        'unique(name)',
        'A tag with the same name already exists.'
    )
