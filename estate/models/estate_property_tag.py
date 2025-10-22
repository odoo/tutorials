from odoo import models, fields


class PropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Real Estate Property Tag"

    name = fields.Char(required=True)

    _unique_name = models.Constraint(
        'UNIQUE(name)', 'The name must be unique.'
    )
