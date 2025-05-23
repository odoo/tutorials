from odoo import models, fields


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = 'Type for categorizing estate properties'

    name = fields.Char('Name', required=True)

    _sql_constraints = [
        ('unique_name', 'UNIQUE(name)', 'A property type name must be unique!'),
    ]
