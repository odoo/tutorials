from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Real Estate Property Tag"

    name = fields.Char('Property Tag', required=True)
    _sql_constraints = [
            ('uniq_tag', 'unique(name)', 'A tag name must be unique.'),
        ]
