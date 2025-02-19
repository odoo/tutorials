from odoo import fields, models


class PropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Property Tags'

    name = fields.Char(required=True)

    _sql_constraints = [
        ("check_unique_tag", "UNIQUE(name)",
         "The tag name should be unique."),
    ]
