from odoo import models, fields


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"
    _order = "name asc"

    _check_unique_name = models.Constraint(
        'UNIQUE (name)',
        'Type names must be unique.',
    )

    name = fields.Char(required=True)
    color = fields.Integer()
