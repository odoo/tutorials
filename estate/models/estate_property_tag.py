from odoo import models, fields


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"
    _order = "name"

    name = fields.Char(required=True)
    color = fields.Integer(string="Color Index")

    _name_uniq = models.Constraint(
        'unique(name)',
        'Property tag name must be unique.',
    )
