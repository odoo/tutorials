from odoo import models, fields


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"
    _order = "name"

    name = fields.Char(required=True)
    color = fields.Integer(string="Color")

    _name_unique = models.Constraint(
        'UNIQUE(name)',
        'Property tag name must be unique.'
    )