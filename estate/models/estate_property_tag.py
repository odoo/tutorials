from odoo import fields, models


class PropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"
    _order = "name"

    name = fields.Char(required=True)
    color = fields.Integer()

    _check_tag_name_unique = models.Constraint(
        'UNIQUE(name)',
        'This tag already exists.',
    )
