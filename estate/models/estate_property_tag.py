from odoo import models, fields


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Real Estate Property Tag"

    name = fields.Char(required=True)

    _check_name = models.Constraint(
        'unique(name)',
        'The tag must be unique',
    )
