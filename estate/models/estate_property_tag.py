from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Estate Property Tag'
    name = fields.Char(required=True)

    _sql_constraints = [
        ('tag_unique', 'UNIQUE (name)', 'Tag must be unique')
    ]
