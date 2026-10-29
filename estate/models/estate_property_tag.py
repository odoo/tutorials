from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"
    _order = "name"

    name = fields.Char(required=True)
    color = fields.Integer(default=1)

    _check_unique_tag = models.Constraint(
        'UNIQUE(name)',
        'A tag with that name already exists.'
    )
