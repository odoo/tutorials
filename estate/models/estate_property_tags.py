from odoo import models, fields


class Estatetags(models.Model):
    _name = 'estate.property.tags'
    _description = 'Estate Property tags'

    name = fields.Char(required=True)

    _check_unique_name = models.Constraint(
        'unique(name)',
        'Property tag name must be unique.'
    )
