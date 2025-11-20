from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"
    _check_name = models.Constraint(
        'UNIQUE(name)',
        'The tag name should be unique!'
    )

    name = fields.Char(required=True)
