from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"

    name = fields.Char(required=True)
    _name_uniq = models.Constraint(
        'UNIQUE (name)',
        "The name of the tag must be unique!",
    )
