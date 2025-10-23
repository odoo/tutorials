from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Define the tags of the property"
    _order = "name"

    _check_unique_tag = models.Constraint(
        'UNIQUE(name)',
        'Tag already exists.',
    )
    name = fields.Char(required=True)
    color = fields.Integer(default=1)
