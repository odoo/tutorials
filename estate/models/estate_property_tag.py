from odoo import models, fields


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = "Estate Property Tag"

    name = fields.Char(string="Tags Name", required=True)

    _check_unique_name = models.Constraint(
        'UNIQUE(name)',
        'Property tag name must be unique.'
    )
