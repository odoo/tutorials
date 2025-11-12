from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Real Estate Property Tag'

    name = fields.Char(required=True)

    _sql_constraints = [
        ('unique_tag_name', 'UNIQUE(name)', 'The tag name must be unique.'),
    ]
