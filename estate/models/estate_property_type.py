from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Type"

    name = fields.Char(required=True)

    _sql_constraints = [
        ('check_name', 'UNIQUE(name)', 'The name must be unique.'),
    ]
