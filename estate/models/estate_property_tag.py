from odoo import models, fields


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Property tags for the estate"
    _order = "name"

    name = fields.Char(required=True)
    color = fields.Integer('Color Index', default=0)

    _name_uniq = models.Constraint(
        'unique(name)',
        'The nae must be unique.',
    )
