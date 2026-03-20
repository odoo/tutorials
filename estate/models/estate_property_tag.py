from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate property tag"
    _order = "name"

    name = fields.Char(required=True)
    color = fields.Integer('Color')
    _check_unique_tag_name = models.Constraint(
        'UNIQUE(name)',
        'This property tag already exists.'
    )
