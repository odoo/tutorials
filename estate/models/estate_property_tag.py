from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Tags describing the property such as 'cozy' and 'renovated'"
    _order = "name"

    name = fields.Char(required=True)
    color = fields.Integer()

    _tag_name_unique = models.Constraint(
        'UNIQUE(name)',
        'Tag names must be unique',
    )
