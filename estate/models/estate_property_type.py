from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "this is the estate property type model"
    name = fields.Char(required=True)
    _sql_constraints = [
        ('check_uniqueness', 'UNIQUE (name)', 'Each property type must be unique')
    ]
