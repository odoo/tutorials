from odoo import fields, models


class PropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Estate Property Tag'

    name = fields.Char(required=True)

    _sql_constraints = [
        ('tag_unique_name', 'unique(name)', 'The tag name must be unique')
    ]
