from odoo import models, fields


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"
    _order = "name"

    _sql_constraints = [
        ('unique_name', 'UNIQUE (name)', 'The tag names should be unique')
    ]

    # Reserved fields
    name = fields.Char(required=True)

    # Model fields
    color = fields.Integer()
