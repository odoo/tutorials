from odoo import models, fields


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Type of real estate property"

    name = fields.Char(required=True)

    _sql_constraints = [
        ('unique_name', 'unique(name)', 'Property types must be unique')
    ]
