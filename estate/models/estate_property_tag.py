from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Property Tag"

    name = fields.Char('Tag', required=True)

    _name_uniq = models.Constraint(
        'unique(name)', 'A tag with the same name already exists.'
    )
