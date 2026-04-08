from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = "estate property tges"
    _order = 'name'

    name = fields.Char(required=True)
    color = fields.Integer()
    _uniq_tag_name = models.Constraint(
        "unique(name)",
        "A tag already exist, tag should be unique.",
    )
