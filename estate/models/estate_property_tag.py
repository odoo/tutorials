from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Estate Property Tag'
    _sql_constraints = [
        ('tag_unique', 'UNIQUE (name)', 'Tag must be unique')
    ]

    name = fields.Char(required=True)
