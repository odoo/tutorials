from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Property Tag"
    _order = 'name'

    name = fields.Char('Tag', required=True)
    color = fields.Integer('Color')

    _name_uniq = models.Constraint(
        'unique(name)', 'A tag with the same name already exists.'
    )
