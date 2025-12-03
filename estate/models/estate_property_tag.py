from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Tags for the estate"
    _order = 'name'

    name = fields.Char('Tag', required=True)
    description = fields.Char('Description')
    color = fields.Integer()

    _unique_tag = models.Constraint(
        'UNIQUE(name)',
        'Tag already exists'
    )
