from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate property types"

    name = fields.Char(required=True)

    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'The property type name must be unique')
    ]
