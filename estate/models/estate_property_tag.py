from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "property tags"

    name = fields.Char(required=True)

    _unique_name = models.Constraint(
        'unique(name)',
        'A tag must have a unique name.',
    )
