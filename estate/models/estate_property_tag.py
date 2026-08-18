from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Real Estate Property Tag"

    name = fields.Char('Tag Name', required=True, translate=True)

    _uniq_name = models.Constraint(
        'UNIQUE(name)',
        'The tag name must be unique'
    )
