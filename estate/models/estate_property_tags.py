from odoo import models, fields


class Estatetags(models.Model):
    _name = 'estate.property.tags'
    _description = "Estate Property tags"
    _order = 'name'

    name = fields.Char(required=True)
    color = fields.Integer()

    _check_unique_name = models.Constraint(
        'unique(name)',
        'Property tag name must be unique.'
    )
