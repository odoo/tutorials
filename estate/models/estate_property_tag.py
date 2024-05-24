from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Estate Property Tag'
    _order = 'name'

    _sql_constraints = [
        ('unique_name', 'UNIQUE (name)', 'The tag names should be unique')
    ]

    name = fields.Char(
        required=True,
    )

    color = fields.Integer()
