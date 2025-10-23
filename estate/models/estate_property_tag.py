from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "property tags"
    _order = "name"

    name = fields.Char(required=True)
    color = fields.Integer()

    _unique_name = models.Constraint(
        'unique(name)',
        'A tag must have a unique name.',
    )
