from odoo import models, fields


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate tags"
    _order = "name"

    name = fields.Char(required=True)
    color = fields.Integer()

    _check_name_is_unique = models.Constraint(
        'unique(name)',
        'The tag name should be unique',
    )
