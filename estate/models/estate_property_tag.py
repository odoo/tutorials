from odoo import fields, models


class EstatePropertyTag(models.Model):

    _name = 'estate.property.tag'
    _description = "Estate Property Tag"

    name = fields.Char(required=True)
    _check_name = models.Constraint(
        'unique (name)',
        'The name must be unique.'
    )
