from odoo import models, fields


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate tags"

    name = fields.Char(required=True)
    _check_name_is_unique = models.Constraint(
        'unique(name)',
        'The tag name should be unique',
    )
